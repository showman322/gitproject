CREATE TABLE IF NOT EXISTS public.groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO public.groups(name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS public.contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES public.groups(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES public.contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile')),
    UNIQUE(contact_id, phone)
);

DO $$
DECLARE
    other_group_id INTEGER;
BEGIN
    SELECT id INTO other_group_id FROM public.groups WHERE name = 'Other';

    IF EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'phonebook'
    ) THEN
        INSERT INTO public.contacts(name, group_id)
        SELECT pb.name, other_group_id
        FROM public.phonebook pb
        ON CONFLICT (name) DO NOTHING;

        INSERT INTO public.phones(contact_id, phone, type)
        SELECT c.id, pb.phone, 'mobile'
        FROM public.phonebook pb
        JOIN public.contacts c ON c.name = pb.name
        ON CONFLICT (contact_id, phone) DO NOTHING;
    END IF;
END $$;
