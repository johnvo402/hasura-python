INSERT INTO "public"."wallet" (user_id, wallet_type_id, min_balance_capacity) VALUES
  ('1v6314mceETIIeJa', 'SP', 0),
  ('1v6314mceETIIeJa', 'VND', 0),
  ('1v6314lUv0gYATaJ', 'SP', 0),
  ('1v6314lUv0gYATaJ', 'VND', 0)
ON CONFLICT (user_id, wallet_type_id) DO NOTHING;


INSERT INTO "public"."user_payment_gateway" (user_id, payment_gateway_id) VALUES
  ('1v6314mceETIIeJa', 'CASH'),
  ('1v6314mceETIIeJa', 'SP'),  
  ('1v6314lUv0gYATaJ', 'CASH'),
  ('1v6314lUv0gYATaJ', 'SP')
ON CONFLICT (user_id, payment_gateway_id) DO NOTHING;
