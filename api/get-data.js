// Vercel Serverless Function: api/get-data.js
// Endpoint: GET /api/get-data?type=all|logs|catalog

const fs = require('fs');
const path = require('path');

module.exports = async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-github-token, x-github-owner, x-github-repo');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

    if (req.method === 'OPTIONS') {
        return res.status(204).end();
    }

    const type = (req.query && req.query.type) ? req.query.type : 'all';
    const githubToken = process.env.GITHUB_TOKEN || req.headers['x-github-token'] || req.query.token || '';
    const githubOwner = process.env.GITHUB_OWNER || req.headers['x-github-owner'] || req.query.repo_owner || 'boasnirut';
    const githubRepo = process.env.GITHUB_REPO || req.headers['x-github-repo'] || req.query.repo || 'order-np';

    // If GitHub token provided, fetch fresh from GitHub API
    if (githubToken) {
        const ghHeaders = {
            'Authorization': `Bearer ${githubToken}`,
            'Accept': 'application/vnd.github+json',
            'User-Agent': 'OrderNP-App',
            'X-GitHub-Api-Version': '2022-11-28'
        };

        async function fetchGitHubFile(filePath) {
            try {
                const url = `https://api.github.com/repos/${githubOwner}/${githubRepo}/contents/${filePath}`;
                const resp = await fetch(url, { headers: ghHeaders });
                if (!resp.ok) return null;
                const json = await resp.json();
                const contentStr = Buffer.from(json.content, 'base64').toString('utf8');
                return JSON.parse(contentStr);
            } catch(e) {
                return null;
            }
        }

        try {
            let result = {};
            if (type === 'all' || type === 'logs') {
                result.logs = await fetchGitHubFile('activity_logs.json') || [];
            }
            if (type === 'all' || type === 'catalog') {
                result.catalog = await fetchGitHubFile('makro_products.json') || null;
            }
            return res.status(200).json({ success: true, source: 'github', data: result });
        } catch(e) {}
    }

    // Fallback: Read local static files bundled with Vercel deployment
    try {
        let result = {};
        if (type === 'all' || type === 'logs') {
            const logsPath = path.join(process.cwd(), 'activity_logs.json');
            if (fs.existsSync(logsPath)) {
                result.logs = JSON.parse(fs.readFileSync(logsPath, 'utf8'));
            } else {
                result.logs = [];
            }
        }
        if (type === 'all' || type === 'catalog') {
            const catPath = path.join(process.cwd(), 'makro_products.json');
            if (fs.existsSync(catPath)) {
                result.catalog = JSON.parse(fs.readFileSync(catPath, 'utf8'));
            }
        }
        return res.status(200).json({ success: true, source: 'local', data: result });
    } catch(err) {
        return res.status(500).json({ success: false, error: err.message });
    }
};
