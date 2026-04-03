CREATE OR REPLACE FUNCTION public.search_phonebook(pattern_text VARCHAR)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.phone
    FROM public.phonebook p
    WHERE p.name ILIKE '%' || pattern_text || '%'
       OR p.phone ILIKE '%' || pattern_text || '%'
    ORDER BY p.id;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.get_phonebook_page(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.name, pb.phone
    FROM public.phonebook pb
    ORDER BY pb.id
    LIMIT p_limit OFFSET p_offset;
END;
$$
LANGUAGE plpgsql;