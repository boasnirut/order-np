// Vercel Serverless Function: api/record-action.js
// Endpoint: POST /api/record-action

module.exports = async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-github-token, x-github-owner, x-github-repo');
    res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');

    if (req.method === 'OPTIONS') {
        return res.status(204).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ success: false, message: 'Method Not Allowed. Use POST.' });
    }

    const payload = req.body || {};
    const actionType = payload.action || 'general_action';
    const actionTitle = payload.title || 'การกระทำในระบบ';
    const actionDetails = payload.details || '';
    const actionData = payload.data || {};
    const updatedProducts = payload.products || null;
    const userName = payload.user || 'ครูนฤทธิ์ (boasnirut)';

    // GitHub configuration from Vercel Environment Variables or request
    const githubToken = process.env.GITHUB_TOKEN || req.headers['x-github-token'] || payload.githubToken || '';
    const githubOwner = process.env.GITHUB_OWNER || req.headers['x-github-owner'] || payload.githubOwner || 'boasnirut';
    const githubRepo = process.env.GITHUB_REPO || req.headers['x-github-repo'] || payload.githubRepo || 'order-np';

    const timestamp = new Date().toISOString();
    const actionId = `act-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`;

    const newLogEntry = {
        id: actionId,
        timestamp: timestamp,
        type: actionType,
        title: actionTitle,
        details: actionDetails,
        user: userName,
        data: actionData
    };

    // If no GitHub token is configured, return the log entry for local storage
    if (!githubToken) {
        return res.status(200).json({
            success: true,
            syncedToGitHub: false,
            message: 'บันทึกประวัติในเครื่องสำเร็จ (ยังไม่ได้ระบุ GitHub Token เพื่อซิงค์ขึ้นคลาวด์)',
            logEntry: newLogEntry
        });
    }

    const ghHeaders = {
        'Authorization': `Bearer ${githubToken}`,
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'OrderNP-App',
        'X-GitHub-Api-Version': '2022-11-28'
    };

    async function getFile(path) {
        const url = `https://api.github.com/repos/${githubOwner}/${githubRepo}/contents/${path}`;
        const resp = await fetch(url, { headers: ghHeaders });
        if (resp.status === 404) return null;
        if (!resp.ok) throw new Error(`GitHub get ${path} failed: ${resp.statusText}`);
        const data = await resp.json();
        const contentStr = Buffer.from(data.content, 'base64').toString('utf8');
        return { sha: data.sha, content: JSON.parse(contentStr) };
    }

    async function putFile(path, contentObj, sha, commitMsg) {
        const url = `https://api.github.com/repos/${githubOwner}/${githubRepo}/contents/${path}`;
        const contentB64 = Buffer.from(JSON.stringify(contentObj, null, 2), 'utf8').toString('base64');
        const body = {
            message: commitMsg,
            content: contentB64,
            committer: {
                name: 'Order NP System',
                email: 'boasnirut@gmail.com'
            }
        };
        if (sha) body.sha = sha;

        const resp = await fetch(url, {
            method: 'PUT',
            headers: ghHeaders,
            body: JSON.stringify(body)
        });
        if (!resp.ok) {
            const errData = await resp.json();
            throw new Error(`GitHub put ${path} failed: ${errData.message || resp.statusText}`);
        }
        return await resp.json();
    }

    try {
        // 1. Update activity_logs.json
        let currentLogs = [];
        let logsSha = null;
        try {
            const fileInfo = await getFile('activity_logs.json');
            if (fileInfo) {
                currentLogs = fileInfo.content;
                logsSha = fileInfo.sha;
            }
        } catch(e) {}

        if (!Array.isArray(currentLogs)) currentLogs = [];
        currentLogs.unshift(newLogEntry);
        // Keep max 500 logs to prevent file bloating
        if (currentLogs.length > 500) currentLogs = currentLogs.slice(0, 500);

        const logsCommit = await putFile(
            'activity_logs.json',
            currentLogs,
            logsSha,
            `log: [${actionType}] ${actionTitle}`
        );

        // 2. If updated catalog products provided, update makro_products.json
        let productsCommit = null;
        if (Array.isArray(updatedProducts) && updatedProducts.length > 0) {
            let prodSha = null;
            try {
                const prodInfo = await getFile('makro_products.json');
                if (prodInfo) prodSha = prodInfo.sha;
            } catch(e) {}

            productsCommit = await putFile(
                'makro_products.json',
                updatedProducts,
                prodSha,
                `catalog: อัปเดตรายการสินค้า (${actionTitle})`
            );
        }

        return res.status(200).json({
            success: true,
            syncedToGitHub: true,
            message: 'บันทึกประวัติและอัปเดตลงใน GitHub เรียบร้อยแล้ว',
            logEntry: newLogEntry,
            commitUrl: logsCommit?.commit?.html_url || ''
        });

    } catch (err) {
        console.error('Error syncing action to GitHub:', err);
        return res.status(200).json({
            success: true,
            syncedToGitHub: false,
            error: err.message,
            message: `บันทึกประวัติในเครื่องสำเร็จ (การซิงค์ GitHub ขัดข้อง: ${err.message})`,
            logEntry: newLogEntry
        });
    }
};
