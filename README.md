# SurveyApi

# Create DB Tables
CREATE TABLE IF NOT EXISTS survey (
    id serial PRIMARY KEY,
    is_live boolean DEFAULT true,
    name character varying(100) NOT NULL,
    discription text,
    start_date date DEFAULT now(),
    end_date date DEFAULT now(),
    survey jsonb NOT NULL,
    questions jsonb);
