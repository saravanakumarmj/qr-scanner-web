create table public.qr_master (
  qr_code text not null,
  cycle_count integer not null default 0,
  qr_printed_ts timestamp with time zone not null,
  flagged boolean not null default false,
  flag_reason text null,
  flag_mode text null,
  flag_device_id text null,
  flagged_ts timestamp with time zone null,
  active_status boolean not null default true,
  discard_user text null,
  discard_device_id text null,
  discard_reason text null,
  discard_ts timestamp with time zone null,
  created_ts timestamp with time zone not null default now(),
  updated_ts timestamp with time zone not null default now(),
  updated_by text not null,
  qr_code_encoded text null,
  constraint qr_master_pkey1 primary key (qr_code),
  constraint qr_master_cycle_count_check check ((cycle_count >= 0)),
  constraint qr_master_discard_reason_check check (
    (
      discard_reason = any (
        array[
          'CYCLE_LIMIT'::text,
          'AGE_LIMIT'::text,
          'DAMAGED'::text
        ]
      )
    )
  ),
  constraint qr_master_flag_mode_check check (
    (
      flag_mode = any (array['AUTO'::text, 'MANUAL'::text])
    )
  ),
  constraint qr_master_flag_reason_check check (
    (
      flag_reason = any (
        array[
          'CYCLE_LIMIT'::text,
          'AGE_LIMIT'::text,
          'DAMAGED'::text
        ]
      )
    )
  )
) TABLESPACE pg_default;

create index IF not exists idx_qr_master_active on public.qr_master using btree (active_status) TABLESPACE pg_default;

create index IF not exists idx_qr_master_flagged on public.qr_master using btree (flagged) TABLESPACE pg_default;

create index IF not exists idx_qr_master_cycle on public.qr_master using btree (cycle_count) TABLESPACE pg_default;

create index IF not exists idx_qr_master_printed on public.qr_master using btree (qr_printed_ts) TABLESPACE pg_default;

create index IF not exists idx_qr_master_updated on public.qr_master using btree (updated_ts) TABLESPACE pg_default;

create index IF not exists idx_qr_master_flagged_ts on public.qr_master using btree (flagged_ts) TABLESPACE pg_default;