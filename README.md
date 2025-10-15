# aistore — README

Short description
-----------------
aistore is a Django + Vue minimal e-commerce project with:
- Products, categories, variants
- Cart with AJAX add/remove, server + client state
- Coupons (validation API)
- Stripe checkout integration
- Featured products and category banners on frontpage
- User signup/login with live password feedback
- Image thumbnails auto-generated

Quick setup
-----------
1. Create and activate a virtualenv (python 3.11 recommended).
2. Install requirements (add your requirements.txt):
   - Django 5.x, Pillow, stripe, Vue (frontend loaded via CDN in templates), Tailwind CSS (if used).
3. Configure environment variables in your OS or .env:
   - DJANGO_SECRET_KEY
   - DEBUG (True/False)
   - DATABASE settings (or set in settings.py)
   - STRIPE_API_KEY_HIDDEN (secret)
   - STRIPE_PUBLISHABLE_KEY (used in templates as `pub_key` context)

Migrations
----------
Run:
- python manage.py makemigrations
- python manage.py migrate

Static and media
----------------
If DEBUG=True, dev static/media served automatically by Django (see settings). Collect static when deploying:
- python manage.py collectstatic

Key models (apps/store/models.py)
--------------------------------
- Category: title, slug, ordering
- Product:
  - category FK, optional parent (variants), title, slug, description
  - price, is_featured, view_count (incremented on product view), num_available
  - image, thumbnail (auto-generated), dateadded
- productImage: extra product images (with thumbnail generation)

Important views & behavior
--------------------------
- apps/store/views.py
  - product_detail: increments `view_count` each visit, builds images array for Vue, supports parent->redirect for variant pages
  - category_detail: lists products in a category
  - search: basic title/description search

- apps/core/views.py
  - frontpage: lists products and featured_products. Featured uses OR logic: `is_featured=True OR view_count > 10` and frontpage limits featured to top 5 (by view_count).
  - featured_products_page: shows all featured products

Cart and APIs (apps/store/api.py & apps/cart)
--------------------------------------------
- add_to_cart_form (POST): accepts form POST (or AJAX via X-Requested-With) and returns JSON for AJAX or redirect for non-AJAX.
- api_add_to_cart (POST JSON): adds to cart, supports quantity/update flag.
- api_remove_from_cart (POST JSON): removes product from cart.
- create_checkout_session (POST JSON): creates Stripe Checkout session, calculates coupon discount, creates Order via `create_order` utility, saves payment_intent.
- checkout (POST JSON): simplified/legacy server checkout (non-Stripe).

Frontend (templates + Vue)
--------------------------
- product_detail.html (apps/store/templates):
  - Vue app `productapp` handles addToCart, buyNow and variant add via AJAX.
  - Uses `cartIds` passed from context to display "Already in Cart" buttons.
  - Thumbnail viewers and image switching for product images.

- cart.html (apps/cart/templates):
  - Vue app `cartapp` manages cart preview, implement increment/decrement, remove, coupon application.
  - Coupon interaction: `GET /api/can_use/?code=...` returns { amount } on valid coupon, otherwise empty/error. UI shows couponError on invalid codes.

- signup.html (apps/userprofile/templates):
  - Live password validation (length, uppercase, lowercase, number, special).
  - Real-time confirm-password matching; visual ✓/✗ feedback.
  - Show/hide password toggles for password1/password2.

- login.html:
  - Show/hide password toggle.

Templating helpers
------------------
- Custom template filter `dict_extras.lookup` used to lookup category_products dict in templates.
- Partials: product_card.html used in many pages for consistent product rendering.

URLs
----
Registered in `aistore/urls.py`:
- Frontpage, contact, about
- Featured page: `/featured/`
- Product detail: `/<category_slug>/<slug>/`
- Category detail: `/<slug>/`
- Cart and cart success, webhook
- Auth: signup, login, logout
- API endpoints:
  - POST `/api/add_to_cart/`
  - POST `/api/remove_from_cart/`
  - POST `/api/create_checkout_session/`
  - GET `/api/can_use/?code=...`
  - POST `/api/checkout/` (non-Stripe fallback)
  - POST `/cart/add/` (form add_to_cart_form)

Stripe
------
- Stripe is used via Checkout Sessions. Configure `STRIPE_API_KEY_HIDDEN` (secret) and expose publishable key to templates as `pub_key`.
- Local webhook forwarding: `stripe listen --forward-to localhost:8000/hooks/`

Security & CSRF
--------------
- AJAX POSTs set header `X-CSRFToken` using the Django template csrf token. Use `credentials: 'same-origin'`.
- Validate and sanitize user inputs on backend for production.

Admin
-----
- Register Product, Category, productImage, Coupon, Order models in admin to manage products, featured flags, coupons, and orders.

Notes for developers
--------------------
- Thumbnail regeneration is implemented in models' `save` method; ensure PIL/Pillow installed.
- `view_count` increments on product_detail view; consider rate-limiting or unique visitor counting if needed.
- For deployment, configure media storage (S3/GCS) for images.
- Add unit tests for APIs, coupon logic, and checkout flows.
- To add new category icons, edit `frontpage.html` icon mapping (simple heuristic by category title).

Troubleshooting
---------------
- FieldError complaining about unknown fields: check models and migrations; run makemigrations and migrate after model changes.
- If Vue components not running, ensure Vue CDN is loaded (usually via base.html) and scripts are placed in `{% block script %}`.

Contributing
------------
- Create a feature branch, add tests, lint, and open a PR.
- Keep UI components (partials) consistent and reuse `partials/product_card.html` for product previews.

Contact / Maintainers
---------------------
- Project maintained in repo root; open issues/PRs for bugs or enhancements.
