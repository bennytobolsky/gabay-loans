module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    res.status(500).json({ error: 'Server missing ANTHROPIC_API_KEY' });
    return;
  }

  const { system, messages } = req.body || {};
  if (typeof system !== 'string' || !Array.isArray(messages) || messages.length === 0) {
    res.status(400).json({ error: 'Invalid request body' });
    return;
  }

  try {
    const anthropicRes = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-5',
        max_tokens: 4096,
        system: [
          { type: 'text', text: system, cache_control: { type: 'ephemeral' } }
        ],
        messages
      })
    });

    const data = await anthropicRes.json();
    res.status(anthropicRes.status).json(data);
  } catch (err) {
    res.status(502).json({ error: 'Upstream request failed' });
  }
};
