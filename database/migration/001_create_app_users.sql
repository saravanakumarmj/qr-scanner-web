create table public.app_users (
  id uuid not null default gen_random_uuid (),
  auth_user_id uuid not null,
  user_id character varying(50) not null,
  full_name character varying(150) not null,
  role character varying(20) not null,
  is_active boolean not null default true,
  created_at timestamp with time zone not null default now(),
  updated_at timestamp with time zone not null default now(),
  location text null,
  constraint app_users_pkey primary key (id),
  constraint app_users_auth_user_id_key unique (auth_user_id),
  constraint app_users_user_id_key unique (user_id),
  constraint app_users_auth_user_id_fkey foreign KEY (auth_user_id) references auth.users (id) on delete RESTRICT,
  constraint app_users_role_check check (
    (
      (role)::text = any (
        (
          array[
            'ADMIN'::character varying,
            'OPERATOR'::character varying,
            'VIEWER'::character varying
          ]
        )::text[]
      )
    )
  )
) TABLESPACE pg_default;