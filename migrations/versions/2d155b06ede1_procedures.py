"""Procedures

Revision ID: 2d155b06ede1
Revises: 03c77835a4c3_
Create Date: 2024-12-05 18:09:08.015365

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2d155b06ede1"
down_revision: Union[str, None] = "03c77835a4c3_"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
    """
        CREATE OR REPLACE PROCEDURE add_provider(
            IN name_n VARCHAR(255),
            IN address_n TEXT,
            IN phone_n VARCHAR(10),
            IN email_n VARCHAR(255)
        )
        LANGUAGE plpgsql AS $$
            BEGIN
                name_n := TRIM(REGEXP_REPLACE(name_n, '\s+', ' ', 'g'));
                address_n := TRIM(REGEXP_REPLACE(address_n, '\s+', ' ', 'g'));
                phone_n := TRIM(REGEXP_REPLACE(phone_n, '\s+', '', 'g'));
                email_n := TRIM(REGEXP_REPLACE(email_n, '\s+', '', 'g'));   

                IF LENGTH(name_n) = 0 THEN
                    RAISE EXCEPTION 'The name cannot be empty';
                END IF;

                IF LENGTH(address_n) = 0 THEN
                    RAISE EXCEPTION 'The address cannot be empty';
                END IF;

                IF NOT phone_n ~ '^[0-9]{10}$' THEN
                    RAISE EXCEPTION 'The phone must be contain 10 number';
                END IF;

                IF NOT email_n ~ '^[^@]+@[^@]+\.[^@]+$' THEN
                    RAISE EXCEPTION 'The mail was entered incorrectly';
                END IF;
                
                INSERT INTO providers (name, address, phone, email) 
                VALUES (name_n, address_n, phone_n, email_n);
            END;
        $$;
    """)
	

    op.execute(
        """
            CREATE OR REPLACE FUNCTION get_all_providers()
            RETURNS TABLE(id INT, name VARCHAR(255), address TEXT, phone VARCHAR(10), email VARCHAR(255)) AS $$
                BEGIN
                    RETURN QUERY SELECT * FROM providers ORDER BY id;
                END;
            $$
            LANGUAGE plpgsql;
        """
    )


    op.execute(
        """
            CREATE OR REPLACE FUNCTION get_provider_by_id(IN id_n TEXT)
            RETURNS TABLE(id INT, name VARCHAR(255), address TEXT, phone VARCHAR(10), email VARCHAR(255)) AS $$
                DECLARE
                    id_new INT;
                BEGIN
                    id_n := TRIM(id_n);

                    IF LENGTH(id_n) = 0 OR NOT id_n ~ '^[0-9]+$' THEN
                        RAISE EXCEPTION 'The identifier must be a positive integer and cannot be empty';
                    END IF;
                    
                    id_new := CAST(id_n AS INT);
                    
                    IF NOT EXISTS (SELECT 1 FROM providers AS p WHERE p.id = id_new) THEN
                        RAISE EXCEPTION 'Provider with id % not found', id_new;
                    END IF;
                    
                    RETURN QUERY SELECT * FROM providers AS p WHERE p.id = id_new;
                END;
            $$ LANGUAGE plpgsql;
        """
    )


    op.execute(
    """
        CREATE OR REPLACE PROCEDURE update_provider(
            IN id_n TEXT, 
            IN name_n VARCHAR(255),
            IN address_n TEXT,
            IN phone_n VARCHAR(10),
            IN email_n VARCHAR(255)
        )
        LANGUAGE plpgsql AS $$
            BEGIN
                IF LENGTH(TRIM(id_n)) = 0 OR NOT TRIM(id_n) ~ '^[0-9]+$' THEN
                    RAISE EXCEPTION 'The provider id must be a positive integer and cannot be empty';
                END IF;
                
                DECLARE
                    id_new INT := CAST(TRIM(id_n) AS INT);
                    
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM providers WHERE id = id_new) THEN
                        RAISE EXCEPTION 'Provider with id % not found', id_new;
                    END IF;

                    IF name_n IS NOT NULL AND name_n <> '' THEN
                        IF TRIM(name_n) <> '' THEN
                            UPDATE providers 
                            SET name = TRIM(REGEXP_REPLACE(name_n, '\s+', ' ', 'g'))
                            WHERE id = id_new;
                        ELSE
                            RAISE EXCEPTION 'The name was entered incorrectly';
                        END IF;
                    END IF;

                    IF address_n IS NOT NULL AND address_n <> '' THEN
                        IF TRIM(address_n) <> '' THEN
                            UPDATE providers 
                            SET address = TRIM(REGEXP_REPLACE(address_n, '\s+', ' ', 'g'))
                            WHERE id = id_new;
                        ELSE
                            RAISE EXCEPTION 'The address was entered incorrectly';
                        END IF;
                    END IF;
                    
                    IF phone_n IS NOT NULL AND phone_n <> '' THEN
                        IF TRIM(phone_n) <> '' AND phone_n ~ '^[0-9]{10}$' THEN
                            UPDATE providers 
                            SET phone = TRIM(REGEXP_REPLACE(phone_n, '\s+', '', 'g'))
                            WHERE id = id_new;
                        ELSE
                            RAISE EXCEPTION 'The phone was entered incorrectly';
                        END IF;
                    END IF;

                    IF email_n IS NOT NULL AND email_n <> '' THEN
                        IF TRIM(email_n) <> '' AND email_n ~ '^[^@]+@[^@]+\.[^@]+$' THEN
                            UPDATE providers 
                            SET email = TRIM(REGEXP_REPLACE(email_n, '\s+', '', 'g'))
                            WHERE id = id_new;
                        ELSE
                            RAISE EXCEPTION 'The email was entered incorrectly';
                        END IF;
                    END IF;
                END;
            END;
        $$;
    """)


    op.execute(
        """
            CREATE OR REPLACE PROCEDURE delete_provider(IN id_n TEXT)
            LANGUAGE plpgsql AS $$
                DECLARE
                    id_new INT;
                BEGIN
                    id_n := NULLIF(TRIM(id_n), '');   -- возвращает null если оба значения равны

                    IF id_n IS NULL OR NOT (id_n ~ '^[0-9]+$') THEN
                        RAISE EXCEPTION 'The provider id must be a positive integer and cannot be empty';
                    END IF;

                    id_new := CAST(id_n AS INT);

                    IF NOT EXISTS (SELECT 1 FROM providers AS p WHERE p.id = id_new) THEN
                        RAISE EXCEPTION 'Providers with ID % not found', id_new;
                    END IF;

                    DELETE FROM providers AS p WHERE p.id = id_new;
                END;
            $$;
        """
    )


    op.execute(
        """
            CREATE OR REPLACE FUNCTION delete_list_providers(ids TEXT[])
            RETURNS INTEGER AS $$
                DECLARE
                    id_new INT;
                    cnt INT := 0; 
                    id TEXT; 
                BEGIN
                    FOREACH id IN ARRAY ids LOOP
                        IF id IS NULL OR NOT id ~ '^[0-9]+$' THEN
                            RAISE NOTICE 'The provider id must be a positive integer and cannot be empty';   -- уведы
                            CONTINUE; 
                        END IF;

                        id_new := id::INT;

                        IF EXISTS (SELECT 1 FROM providers AS p WHERE p.id = id_new) THEN
                            DELETE FROM providers AS p WHERE p.id = id_new;
                            cnt := cnt + 1;  
                        ELSE
                            RAISE NOTICE 'The providers with id % was not found', id_new;
                        END IF;

                    END LOOP;
                    RAISE NOTICE 'Removed providers: %', cnt;

                    RETURN cnt;  
                END;
            $$ LANGUAGE plpgsql;
        """
    )



def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS add_provider(VARCHAR(255), TEXT, VARCHAR(10), VARCHAR(255));")
    op.execute("DROP FUNCTION IF EXISTS get_all_providers();")
    op.execute("DROP FUNCTION IF EXISTS get_provider_by_id(TEXT);")
    op.execute("DROP PROCEDURE IF EXISTS update_provider(TEXT, VARCHAR(255), TEXT, VARCHAR(10), VARCHAR(255));")
    op.execute("DROP PROCEDURE IF EXISTS delete_provider(TEXT);")
    op.execute("DROP FUNCTION IF EXISTS delete_list_providers(TEXT[]);")
