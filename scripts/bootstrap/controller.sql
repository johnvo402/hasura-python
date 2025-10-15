INSERT INTO api_key(id, api_key, type, comment, allowed_fqdn) VALUES
  (1, 'fm2ss367h1206socg73lqbd4aa5cb82b8deobissoob6mnm8r36necrpm4ho1rd', 'app', 'Mobile app', NULL)
  ON CONFLICT DO NOTHING;
