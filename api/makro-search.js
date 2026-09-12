// Vercel Serverless Function: api/makro-search.js
// Endpoint: /api/makro-search?q=929370

module.exports = async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

    if (req.method === 'OPTIONS') {
        return res.status(204).end();
    }

    let q = (req.query && req.query.q) ? String(req.query.q).trim() : '';
    if (!q) {
        return res.status(400).json({ success: false, message: 'กรุณาระบุรหัสสินค้าหรือชื่อสินค้า Makro' });
    }

    q = q.replace(/^["'“‘\[\(•\s\-_*]+|["'”’\]\)•\s\-_*]+$/g, '').trim();

    // Extract Makro ID or query if full URL is pasted
    const urlMatch = q.match(/makro\.pro\/(?:[a-z]{2}\/)?p\/([0-9]+)/i);
    if (urlMatch) {
        q = urlMatch[1];
    } else {
        const urlSearchMatch = q.match(/makro\.pro\/(?:[a-z]{2}\/)?c\/search\?.*?[?&]q=([^&]+)/i);
        if (urlSearchMatch) {
            try { q = decodeURIComponent(urlSearchMatch[1]).trim(); } catch(e) { q = urlSearchMatch[1].trim(); }
        }
    }

    async function doMakroFetch(term) {
        const searchUrl = `https://www.makro.pro/c/search?q=${encodeURIComponent(term)}`;
        const response = await fetch(searchUrl, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept-Language': 'th,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
        });
        if (!response.ok) return [];
        const html = await response.text();
        const match = html.match(/<script id="__NEXT_DATA__" type="application\/json">([\s\S]*?)<\/script>/);
        if (!match) return [];
        const data = JSON.parse(match[1]);
        return data?.props?.pageProps?.initialSearchResult?.hits || [];
    }

    try {
        let hits = await doMakroFetch(q);
        if (hits.length === 0 && q.includes(' ')) {
            const words = q.split(/\s+/).filter(Boolean);
            if (words.length > 2) {
                hits = await doMakroFetch(words.slice(0, 2).join(' '));
            }
        }

        const results = hits.map(h => {
            const doc = h.document || {};
            const cats = (doc.categories || []).join(' ').toLowerCase();
            const title = doc.title || doc.productName || '';

            let category = 'เครื่องปรุง-ทั่วไป';
            if (cats.includes('snack') || cats.includes('biscuit') || cats.includes('candy') || cats.includes('chocolate') || cats.includes('chip') || /ขนม|ช็อก|เวเฟอร์|มันฝรั่ง|คุกกี้|ลูกอม/.test(title)) {
                category = 'ขนม';
            } else if (cats.includes('beverage') || cats.includes('drink') || cats.includes('coffee') || cats.includes('tea') || cats.includes('water') || cats.includes('milk') || cats.includes('juice') || /น้ำ|นม|กาแฟ|ชา|โซดา|โออิชิ|โค้ก|เป๊ปซี่/.test(title)) {
                category = 'เครื่องดื่ม';
            }

            const rawPrice = doc.displayPrice !== undefined ? doc.displayPrice : (doc.originalPrice !== undefined ? doc.originalPrice : 0);
            const price = parseFloat(rawPrice) || 0;

            let imgUrl = '';
            if (Array.isArray(doc.images) && doc.images.length > 0) {
                imgUrl = doc.images[0];
            } else if (doc.image) {
                imgUrl = doc.image;
            }

            return {
                code: String(doc.makroId || '').trim(),
                name: title.trim(),
                price: price,
                barcode: String(doc.itemBarCode || (doc.itemBarCodes ? doc.itemBarCodes[0] : '')).trim(),
                image: imgUrl,
                category: category,
                brand: doc.brand || '',
                unit: doc.unitType || 'Pack'
            };
        });

        return res.status(200).json({
            success: true,
            query: q,
            count: results.length,
            hits: results
        });
    } catch (err) {
        return res.status(500).json({ success: false, error: err.message });
    }
};
