// 排行榜 API:GET 拉榜 / POST 提交成绩
// 存储:Netlify Blobs(key: leaderboard)
const { getStore, connectLambda } = require('@netlify/blobs');

const MAX_ENTRIES = 100;

function sanitizeName(raw) {
  if (typeof raw !== 'string') return '车手';
  const s = raw.trim().replace(/[<>]/g, '').slice(0, 12);
  return s || '车手';
}

exports.handler = async (event) => {
  // Lambda 兼容模式:必须先 connectLambda(event) 再 getStore
  connectLambda(event);
  const store = getStore('leaderboard');

  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json; charset=utf-8',
  };
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 204, headers, body: '' };
  }

  try {
    if (event.httpMethod === 'GET') {
      const raw = await store.get('leaderboard', { type: 'text' });
      const list = raw ? JSON.parse(raw) : [];
      return { statusCode: 200, headers, body: JSON.stringify(list) };
    }

    if (event.httpMethod === 'POST') {
      let body;
      try { body = JSON.parse(event.body || '{}'); }
      catch (e) { return { statusCode: 400, headers, body: JSON.stringify({ error: 'bad json' }) }; }

      const name = sanitizeName(body.name);
      const score = Math.max(0, Math.floor(Number(body.score) || 0));
      const carId = typeof body.carId === 'number' ? body.carId : 0;
      const ts = Date.now();

      const raw = await store.get('leaderboard', { type: 'text' });
      const list = raw ? JSON.parse(raw) : [];
      list.push({ name, score, carId, ts });
      list.sort((a, b) => b.score - a.score);
      const top = list.slice(0, MAX_ENTRIES);
      await store.set('leaderboard', JSON.stringify(top));

      const rank = top.findIndex(x => x.ts === ts && x.name === name);
      return { statusCode: 200, headers, body: JSON.stringify({ ok: true, rank: rank >= 0 ? rank + 1 : -1, list: top }) };
    }

    return { statusCode: 405, headers, body: JSON.stringify({ error: 'method not allowed' }) };
  } catch (err) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: String(err && err.message || err) }) };
  }
};
