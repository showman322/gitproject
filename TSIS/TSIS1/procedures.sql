CREATE OR REPLACE PROCEDURE public.add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    IF p_phone !~ '^\+?[0-9]{6,15}$' THEN
        RAISE EXCEPTION 'Invalid phone number: %', p_phone;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type: %. Use home, work, or mobile', p_type;
    END IF;

    SELECT id INTO v_contact_id
    FROM public.contacts
    WHERE lower(name) = lower(p_contact_name);

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found: %', p_contact_name;
    END IF;

    INSERT INTO public.phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type)
    ON CONFLICT (contact_id, phone) DO UPDATE SET type = EXCLUDED.type;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE public.move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    INSERT INTO public.groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM public.groups
    WHERE lower(name) = lower(p_group_name);

    UPDATE public.contacts
    SET group_id = v_group_id
    WHERE lower(name) = lower(p_contact_name);

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact not found: %', p_contact_name;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.search_contacts(p_query TEXT)
RETURNS TABLE(
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT,
    created_at TIMESTAMP
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name AS group_name,
        COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.type, p.phone), '') AS phones,
        c.created_at
    FROM public.contacts c
    LEFT JOIN public.groups g ON g.id = c.group_id
    LEFT JOIN public.phones p ON p.contact_id = c.id
    GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
    HAVING
        c.name ILIKE '%' || p_query || '%'
        OR COALESCE(c.email, '') ILIKE '%' || p_query || '%'
        OR COALESCE(g.name, '') ILIKE '%' || p_query || '%'
        OR COALESCE(string_agg(p.phone, ' '), '') ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.get_contacts_page(
    p_limit INTEGER,
    p_offset INTEGER,
    p_sort_by TEXT DEFAULT 'name',
    p_group TEXT DEFAULT NULL
)
RETURNS TABLE(
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT,
    created_at TIMESTAMP
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name AS group_name,
        COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.type, p.phone), '') AS phones,
        c.created_at
    FROM public.contacts c
    LEFT JOIN public.groups g ON g.id = c.group_id
    LEFT JOIN public.phones p ON p.contact_id = c.id
    WHERE p_group IS NULL OR lower(g.name) = lower(p_group)
    GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
    ORDER BY
        CASE WHEN p_sort_by = 'name' THEN c.name END ASC,
        CASE WHEN p_sort_by = 'birthday' THEN c.birthday END ASC NULLS LAST,
        CASE WHEN p_sort_by = 'date' THEN c.created_at END DESC,
        c.id ASC
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
