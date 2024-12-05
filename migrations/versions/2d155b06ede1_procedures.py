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
    #! Исправить
    op.execute(
    """
        CREATE OR REPLACE PROCEDURE add_provider(
            IN name TEXT,
            IN address TEXT,
            IN phone TEXT
            IN email TEXT
        )
        LANGUAGE plpgsql AS $$
            BEGIN
                name := TRIM(name);
                address := TRIM(address);
                            
                INSERT INTO manufacturer (title_country, address_of_manufacturer, contact_list) 
                VALUES (name, address, phone, email);
            END;
        $$;
    """)
	
    op.execute(
        """
            CREATE OR REPLACE PROCEDURE get_all_providers()
            LANGUAGE plpgsql AS $$
                BEGIN
                    RETURN QUERY SELECT * FROM providers;
                END;
            $$;
        """
    )

    #! Исправить
    op.execute(
        """
            CREATE OR REPLACE FUNCTION get_provider_by_id(IN id TEXT)
            RETURNS TABLE(id INT, name VARCHAR(255), address TEXT, phone TEXT, email TEXT) AS $$
                DECLARE
                    id_new INT;
                BEGIN
                    id := TRIM(id);

                    IF LENGTH(id) = 0 OR NOT id ~ '^[0-9]+$' THEN
                        RAISE EXCEPTION 'The identifier must be a positive integer and cannot be empty';
                    END IF;
                    
                    id_new := CAST(id AS INT);
                    
                    IF NOT EXISTS (SELECT 1 FROM providers WHERE providers.id = id_new) THEN
                        RAISE EXCEPTION 'Provider with id % not found', id_new;
                    END IF;
                    
                    RETURN QUERY SELECT * FROM providers WHERE providers.id = id_new;
                END;
            $$ LANGUAGE plpgsql;
        """
    )

    #! Исправить
    op.execute(
    """
        CREATE OR REPLACE PROCEDURE update_provider(
            IN id TEXT, 
            IN name TEXT,
            IN address TEXT,
            IN phone TEXT
            IN email TEXT
        )
        LANGUAGE plpgsql AS $$
            BEGIN
                IF LENGTH(TRIM(p_manufacturer_id)) = 0 OR NOT TRIM(p_manufacturer_id) ~ '^[0-9]+$' THEN
                    RAISE EXCEPTION 'The provider id must be a positive integer and cannot be empty';
                END IF;
                DECLARE
                    id_new INT := CAST(TRIM(id) AS INT);
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM providers WHERE id = id_new) THEN
                        RAISE EXCEPTION 'Provider with id % not found', id_new;
                    END IF;

                    IF name IS NOT NULL AND TRIM(name) <> '' THEN
                        UPDATE providers 
                        SET name = TRIM(name)
                        WHERE id = id_new;
                    END IF;

                    IF address IS NOT NULL AND TRIM(address) <> '' THEN
                        UPDATE providers 
                        SET address = TRIM(address)
                        WHERE id = id_new;
                    END IF;
                    
                    IF phone IS NOT NULL AND TRIM(phone) <> '' THEN
                        UPDATE providers 
                        SET phone = TRIM(phone)
                        WHERE id = id_new;
                    END IF;
                END;
            END;
        $$;
    """)

    #! Исправить
    op.execute(
        """
            CREATE OR REPLACE PROCEDURE delete_provider(IN id TEXT)
            LANGUAGE plpgsql AS $$
            DECLARE
                id_new INT;
            BEGIN
                id_new := NULLIF(TRIM(id), '');
                IF id_new IS NULL OR NOT (id ~ '^[0-9]+$') THEN
                    RAISE EXCEPTION 'The provider id must be a positive integer and cannot be empty';
                END IF;

                id_new := CAST(id_new AS INT);

                IF NOT EXISTS (SELECT 1 FROM providers WHERE providers.providers_id = id_new) THEN
                    RAISE EXCEPTION 'Providers with ID % not found', id_new;
                END IF;

                DELETE FROM providers WHERE providers.providers_id = id_new;
            END;
            $$;
        """
    )

    #! Исправить
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
                        RAISE NOTICE 'The provider id must be a positive integer and cannot be empty', id;
                        CONTINUE; 
                    END IF;

                    id_new := id::INT;

                    IF EXISTS (SELECT 1 FROM providers WHERE id = id_new) THEN
                        DELETE FROM providers WHERE id = id_new;
                        cnt := cnt + 1;  
                    ELSE
                        RAISE NOTICE 'The providers with id % was not found.', id_new;
                    END IF;

                END LOOP;
                RAISE NOTICE 'Removed providers: %', cnt;

                RETURN cnt;  
            END;
            $$ LANGUAGE plpgsql;
        """
    )


def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS add_provider(TEXT, TEXT, TEXT, TEXT);")
    op.execute("DROP PROCEDURE IF EXISTS get_all_providers();")
    op.execute("DROP PROCEDURE IF EXISTS get_provider_by_id(TEXT);")
    op.execute("DROP PROCEDURE IF EXISTS update_provider(TEXT, TEXT, TEXT, TEXT, TEXT);")
    op.execute("DROP PROCEDURE IF EXISTS delete_provider(TEXT);")
    op.execute("DROP PROCEDURE IF EXISTS delete_list_providers(TEXT[]);")
