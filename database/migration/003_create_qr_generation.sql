create table public.qr_generation (
  generation_id uuid not null default gen_random_uuid(),
  generation_date date not null default current_date,
  start_qr_code text not null,
  end_qr_code text not null,
  quantity integer not null,
  generated_by text not null,
  generated_ts timestamp with time zone not null default now(),
  print_status text not null default 'PENDING',
  created_ts timestamp with time zone not null default now(),

  constraint qr_generation_pkey primary key (generation_id),

  constraint qr_generation_quantity_check
    check (quantity > 0),

  constraint qr_generation_print_status_check
    check (
      print_status = any (
        array[
          'PENDING'::text,
          'PARTIAL'::text,
          'COMPLETED'::text
        ]
      )
    )
);

create index if not exists idx_qr_generation_date
  on public.qr_generation using btree (generation_date);

create index if not exists idx_qr_generation_generated_by
  on public.qr_generation using btree (generated_by);

create index if not exists idx_qr_generation_print_status
  on public.qr_generation using btree (print_status);

create index if not exists idx_qr_generation_generated_ts
  on public.qr_generation using btree (generated_ts);