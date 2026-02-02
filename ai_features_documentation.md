# 🤖 AI Features - Detailed Method Documentation

## সহজ ভাষায় AI ফিচার ব্যাখ্যা (AI Features Explained Simply)

---

# 📍 Part 1: AI Chatbot

## ফাইলসমূহ (Files)

---

### 🎯 `orchestrator.py` - Main Brain

**কী করে:** Chatbot-এর main controller। সব কাজ coordinate করে।

#### Class: `ChatbotOrchestrator`

| Method | কী করে | Input | Output |
|--------|--------|-------|--------|
| `__init__()` | Initialize করে, settings load করে | - | - |
| `_is_followup_question(question)` | "yes", "no", "compare" এমন follow-up কিনা check করে | question text | True/False |
| `generate_answer(question, chat_history, user)` | Customer question থেকে answer তৈরি করে | question, history, user | (answer, citations) |

#### `generate_answer()` কীভাবে কাজ করে:

```
1. Intent detect করে (product? order? coupon?)
2. Follow-up check করে
3. RAG থেকে knowledge খোঁজে (if needed)
4. Product/Order data খোঁজে (if needed)
5. LLM-এ পাঠায়, answer পায়
6. Answer ও citations return করে
```

---

### 🎯 `intent.py` - Intent Detection

**কী করে:** Customer কী চাইছে detect করে।

#### Class: `Intent` (Enum)

| Intent | মানে |
|--------|------|
| `GENERAL` | সাধারণ প্রশ্ন |
| `PRODUCT_INFO` | Product সম্পর্কে জানতে চায় |
| `ORDER_STATUS` | Order status জানতে চায় |
| `COUPON` | Discount/coupon চায় |
| `SHIPPING` | Shipping সম্পর্কে জানতে চায় |
| `GREETING` | Hello, Hi বলছে |

#### Class: `IntentClassifier`

| Method | কী করে | Input | Output |
|--------|--------|-------|--------|
| `classify(question)` | Question analyze করে intent বের করে | question text | IntentResult (intent + keyword) |

**Pattern Examples:**
- "laptop আছে?" → `PRODUCT_INFO`
- "আমার order কোথায়?" → `ORDER_STATUS`
- "discount code আছে?" → `COUPON`
- "Hello" → `GREETING`

---

### 🎯 `rag.py` - Vector Database

**কী করে:** Knowledge base-এ semantic search করে। ChromaDB ব্যবহার করে।

#### Class: `VectorIndex`

| Method | কী করে | Input | Output |
|--------|--------|-------|--------|
| `__init__(persist_directory, embedding_model)` | Vector store load করে | directory path, model name | - |
| `similarity_search(query, k)` | Query-র similar documents খোঁজে | query text, result count | List of Documents |
| `as_snippets(documents)` | Documents থেকে text বের করে | documents | List of strings |
| `as_citations(documents)` | Documents থেকে citation তৈরি করে | documents | List of dicts |

#### Standalone Functions:

| Function | কী করে |
|----------|--------|
| `build_vector_index(documents, persist_directory, embedding_model)` | নতুন vector store তৈরি করে |
| `get_vector_index(persist_directory, embedding_model)` | Existing store load করে (cached) |

---

### 🎯 `tools.py` - Data Fetchers

**কী করে:** Live data (products, orders, coupons) fetch করে।

| Function | কী করে | Input | Output |
|----------|--------|-------|--------|
| `product_lookup_context(question, limit, user)` | ML search দিয়ে products খোঁজে | question, limit, user | List of product dicts |
| `order_status_context(user, question, limit)` | User-এর orders খোঁজে | user, question, limit | List of order dicts |
| `coupon_context(question)` | Active coupons খোঁজে | question | List of coupon dicts |
| `gather_dynamic_context(intent, question, user)` | Intent অনুযায়ী correct function call করে | intent, question, user | Combined context list |

---

# 📍 Part 2: AI Recommendations

## ফাইলসমূহ (Files)

---

### 🎯 `recommender.py` - ML Models

**কী করে:** Product recommendations generate করে।

---

#### Class: `ContentBasedRecommender`

**Algorithm:** TF-IDF + Cosine Similarity
**কীভাবে কাজ করে:** Product-এর title, description, category, price দেখে similar products খোঁজে।

| Method | কী করে | Input | Output |
|--------|--------|-------|--------|
| `__init__()` | TF-IDF vectorizer initialize | - | - |
| `prepare_features(products)` | Products থেকে text features তৈরি করে | products list | features list |
| `train(products)` | Model train করে | products list | - |
| `get_recommendations(product_id, n)` | Similar products খোঁজে | product ID, count | List of (id, score) |
| `save(filepath)` | Model file-এ save করে | filepath | - |
| `load(filepath)` | Model file থেকে load করে | filepath | True/False |

---

#### Class: `CollaborativeFilteringRecommender`

**Algorithm:** SVD Matrix Factorization
**কীভাবে কাজ করে:** User behavior (view, click, purchase) analyze করে pattern খোঁজে।

| Method | কী করে | Input | Output |
|--------|--------|-------|--------|
| `__init__(n_components)` | SVD model initialize | components count | - |
| `train(interactions)` | User interactions দিয়ে train করে | interactions list | - |
| `get_recommendations(product_id, n)` | Similar products খোঁজে | product ID, count | List of (id, score) |
| `save(filepath)` | Model save করে | filepath | - |
| `load(filepath)` | Model load করে | filepath | True/False |

**Interaction Data Format:**
```python
{
    'user_id': 123,
    'product_id': 456,
    'weight': 1.0  # View=1, Cart=3, Purchase=5
}
```

---

#### Class: `HybridRecommender`

**কীভাবে কাজ করে:** Both models combine করে better results দেয়।

| Method | কী করে | Input | Output |
|--------|--------|-------|--------|
| `__init__(content_weight, collab_weight)` | Both models initialize, weights set | weights (0.6, 0.4) | - |
| `train(products, interactions)` | Both models train করে | products, interactions | - |
| `get_recommendations(product_id, n)` | Combined recommendations | product ID, count | List of product IDs |
| `save()` | Both models save | - | - |
| `load()` | Both models load | - | True/False |

**Score Calculation:**
```
Final Score = (Content Score × 0.6) + (Collab Score × 0.4)
```

---

### 🎯 `training.py` - Model Training

| Function | কী করে |
|----------|--------|
| `train_recommendation_models()` | সব products ও interactions নিয়ে model train করে |
| `create_synthetic_interactions(products)` | Fake interaction data তৈরি করে (initial training-এর জন্য) |

---

### 🎯 `views.py` - API

| Endpoint | Method | কী করে |
|----------|--------|--------|
| `/api/recommendations/<product_id>/` | GET | Product-এর recommendations return করে |

---

# 📍 Part 3: AI Search

## ফাইলসমূহ (Files)

---

### 🎯 `ml_search.py` - Search Engine

**কী করে:** Semantic + Keyword hybrid search করে।

#### Class: `MLSearchEngine`

---

#### Basic Methods:

| Method | কী করে | Input | Output |
|--------|--------|-------|--------|
| `__init__()` | Initialize, model path set | - | - |
| `load_model()` | Sentence Transformer model load করে | - | model |
| `create_product_text(product)` | Product থেকে searchable text তৈরি | product | text string |
| `generate_embedding(text)` | Text থেকে vector তৈরি করে | text | numpy array (384 dimensions) |

---

#### Indexing Methods:

| Method | কী করে | Input | Output |
|--------|--------|-------|--------|
| `index_product(product)` | Single product index করে | product | True/False |
| `index_all_products(force_reindex)` | সব products index করে | force flag | - |
| `load_embeddings()` | সব embeddings memory-তে load করে | - | dict {id: vector} |

---

#### Search Methods:

| Method | কী করে | Input | Output |
|--------|--------|-------|--------|
| `semantic_search(query, limit, category_filter, user)` | AI দিয়ে meaning বুঝে search | query, limit, category, user | List of (product, score) |
| `keyword_search(query, category_filter)` | Traditional text matching | query, category | List of products |
| `hybrid_search(query, limit, category_filter, user)` | Both combine করে best results | query, limit, category, user | List of products |

**Hybrid Search Scoring:**
```
Final = (Semantic × 0.7) + (Keyword × 0.3) + (Popularity × 0.1)
```

---

#### Analytics Methods:

| Method | কী করে | Input | Output |
|--------|--------|-------|--------|
| `get_search_suggestions(query, limit)` | Autocomplete suggestions | partial query, limit | List of query strings |
| `track_search(query, results_count, user, ip, user_agent)` | Search query record করে | query details | SearchQuery object |
| `track_click(search_query, product, position)` | Click record করে | query, product, position | - |

---

### 🎯 `views.py` - Search Views

| Endpoint | Method | কী করে |
|----------|--------|--------|
| `/search/` | GET | Search results page |
| `/search/api/autocomplete/` | GET | Autocomplete suggestions (JSON) |

---

# 🔄 Data Flow Diagrams

## Chatbot Flow:

```
User Question
    ↓
Intent Classification (intent.py)
    ↓
┌─────────────────────────────────────┐
│  Product? → ML Search              │
│  Order?   → Database Query         │
│  Coupon?  → Coupon Query           │
│  General? → RAG Vector Search      │
└─────────────────────────────────────┘
    ↓
Context + Question → LLM
    ↓
Answer + Citations
```

## Search Flow:

```
User Query
    ↓
Generate Query Embedding (384-dim vector)
    ↓
Compare with all Product Embeddings
    ↓
Filter by Similarity Score (> 35%)
    ↓
Add Keyword Search Results
    ↓
Add Popularity Boost
    ↓
Return Ranked Results
```

## Recommendation Flow:

```
Product Page View
    ↓
Get Product ID
    ↓
┌───────────────────────────────────┐
│ Content-Based: Similar features   │
│ Collaborative: User patterns      │
└───────────────────────────────────┘
    ↓
Combine Scores (60% + 40%)
    ↓
Top 6 Recommendations
```

---

*এই documentation দিয়ে AI system-এর সব method বুঝতে পারবেন।*
