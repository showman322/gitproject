CREATE OR REPLACE PROCEDURE public.insert_or_update_user(
    p_name VARCHAR,
    p_phone VARCHAR
)
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM public.phonebook
        WHERE name = p_name
    ) THEN
        UPDATE public.phonebook
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO public.phonebook(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE public.insert_many_users(
    IN p_names VARCHAR[],
    IN p_phones VARCHAR[],
    INOUT wrong_data TEXT
)
AS $$
DECLARE
    i INT;
BEGIN
    wrong_data := '';

    IF array_length(p_names, 1) IS NULL OR array_length(p_phones, 1) IS NULL THEN
        wrong_data := 'Input arrays are empty';
        RETURN;
    END IF;

    IF array_length(p_names, 1) <> array_length(p_phones, 1) THEN
        wrong_data := 'Arrays must have the same length';
        RETURN; 
    END IF;

    FOR i IN 1 .. array_length(p_names, 1)
    LOOP
        IF p_phones[i] ~ '^\+?[0-9]{6,15}$' THEN
            IF EXISTS (
                SELECT 1
                FROM public.phonebook
                WHERE name = p_names[i]
            ) THEN
                UPDATE public.phonebook
                SET phone = p_phones[i]
                WHERE name = p_names[i];
            ELSE
                INSERT INTO public.phonebook(name, phone)
                VALUES (p_names[i], p_phones[i]);
            END IF;
        ELSE
            wrong_data := wrong_data || '(' || p_names[i] || ', ' || p_phones[i] || '); ';
        END IF;
    END LOOP;
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE public.delete_user(p_value VARCHAR)
AS $$
BEGIN
    DELETE FROM public.phonebook
    WHERE name = p_value OR phone = p_value;
END;
$$
LANGUAGE plpgsql;