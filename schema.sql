CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name  VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS credits (
    user_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    credits INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

INSERT INTO users (email, name) VALUES
('alice@example.com', 'Alice'),
('bob@example.com', 'Bob')
ON CONFLICT DO NOTHING;

INSERT INTO credits (user_id, credits)
SELECT u.user_id, 0 FROM users u
LEFT JOIN credits c ON c.user_id = u.user_id
WHERE c.user_id IS NULL;
