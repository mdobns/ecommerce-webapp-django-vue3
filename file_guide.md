# 📁 ShopSense - File-by-File Guide
## প্রতিটি ফাইল কী করে (What Each File Does)

---

## 🔧 Main Project Files (`shopsense/`)

| File | কী করে |
|------|--------|
| `settings.py` | সব settings - database, payment keys, security |
| `urls.py` | কোন URL কোন page দেখাবে তা define করে |
| `wsgi.py` | Production server-এ deploy করতে লাগে |

---

## 🛒 Cart App (`apps/cart/`)

| File | কী করে |
|------|--------|
| `cart.py` | Cart class - add, remove, clear items |
| `views.py` | Cart page, checkout page, success page দেখায় |
| `webhook.py` | Stripe payment confirm হলে order update করে |
| `bkash_integration.py` | bKash payment create ও verify করে |
| `models.py` | Cart-এর database models (empty) |
| `urls.py` | Cart-এর URLs |
| `apps.py` | App configuration |
| `context_processors.py` | Navbar-এ cart count দেখায় |

---

## 🤖 Chatbot App (`apps/chatbot/`)

| File | কী করে |
|------|--------|
| `views.py` | Chat API - customer question নেয়, answer দেয় |
| `apps.py` | Server start-এ knowledge base তৈরি করে |
| `urls.py` | Chatbot API URLs |
| `models.py` | Chat history save করতে পারে |

### Chatbot Services (`apps/chatbot/services/`)

| File | কী করে |
|------|--------|
| `orchestrator.py` | Main brain - question বুঝে answer তৈরি করে |
| `rag.py` | Vector database - semantic search |
| `context.py` | Products/orders থেকে knowledge তৈরি |
| `tools.py` | Product lookup, order status check |
| `intent.py` | Customer কী চাইছে detect করে |

---

## 🏠 Core App (`apps/core/`)

| File | কী করে |
|------|--------|
| `views.py` | Homepage, contact, about page দেখায় |
| `models.py` | ContactMessage - contact form data save |
| `admin.py` | Admin panel-এ contact messages দেখা |
| `urls.py` | Core pages-এর URLs |

---

## 🎫 Coupon App (`apps/coupon/`)

| File | কী করে |
|------|--------|
| `models.py` | Coupon model - code, discount%, limit |
| `api.py` | Coupon valid কিনা check করে |
| `admin.py` | Admin panel-এ coupon manage |

---

## 📋 Order App (`apps/order/`)

| File | কী করে |
|------|--------|
| `models.py` | Order, OrderItem models |
| `utils.py` | Cart থেকে Order তৈরি করে |
| `admin.py` | Admin panel-এ orders manage |

---

## ⭐ Recommendations App (`apps/recommendations/`)

| File | কী করে |
|------|--------|
| `recommender.py` | ML models - similar products খুঁজে |
| `training.py` | ML model train করে |
| `views.py` | Recommendation API |
| `models.py` | ProductView, ProductInteraction track |
| `apps.py` | Server start-এ model train করে |

---

## 🔍 Search App (`apps/search/`)

| File | কী করে |
|------|--------|
| `ml_search.py` | AI search engine - semantic + keyword |
| `views.py` | Search results page, autocomplete |
| `models.py` | ProductEmbedding, SearchQuery, SearchClick |
| `urls.py` | Search URLs |

---

## 🏪 Store App (`apps/store/`)

| File | কী করে |
|------|--------|
| `models.py` | Category, Product, Image models |
| `views.py` | Product detail, category page দেখায় |
| `api.py` | Add to cart, Stripe checkout |
| `admin.py` | Admin panel-এ products manage |

---

## 👤 User Profile App (`apps/userprofile/`)

| File | কী করে |
|------|--------|
| `views.py` | Signup, my account page |
| `forms.py` | Signup form validation |
| `models.py` | UserAddress - saved addresses |
| `admin.py` | Admin panel-এ users দেখা |

---

## 📄 Common Files (সব app-এ আছে)

| File | কী করে |
|------|--------|
| `__init__.py` | Python package marker (empty) |
| `apps.py` | App configuration |
| `admin.py` | Admin panel setup |
| `models.py` | Database tables define |
| `views.py` | Page/API logic |
| `urls.py` | URL routing |
| `tests.py` | Testing (optional) |

---

## 📂 Templates (`apps/*/templates/`)

HTML files - প্রতিটি page-এর design

| Template | Page |
|----------|------|
| `frontpage.html` | Homepage |
| `product_detail.html` | Single product page |
| `cart.html` | Shopping cart |
| `checkout.html` | Checkout form |
| `success.html` | Order success |
| `payment_bkash.html` | bKash payment gateway |
| `myaccount.html` | User dashboard |
| `search_results.html` | Search results |

---

## 🗄️ Other Files

| File | কী করে |
|------|--------|
| `manage.py` | Django commands চালায় |
| `requirements.txt` | Python packages list |
| `db.sqlite3` | Database file |
| `render.yaml` | Cloud deploy config |
| `build.sh` | Deploy script |

---

*এই guide দিয়ে বুঝতে পারবেন কোন file কী কাজ করে।*
