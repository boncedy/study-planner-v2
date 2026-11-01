CREATE TABLE IF NOT EXISTS study_sessions (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  student_id TEXT NOT NULL CHECK (char_length(student_id) BETWEEN 1 AND 30),
  subject TEXT NOT NULL CHECK (char_length(subject) BETWEEN 1 AND 80),
  goal TEXT NOT NULL CHECK (char_length(goal) BETWEEN 1 AND 200),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
