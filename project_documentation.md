# 🛍️ ShopSense - সিস্টেম ডকুমেন্টেশন
## E-commerce Website Overview

---

## এটা কি? (What is ShopSense?)

ShopSense হলো একটি সম্পূর্ণ e-commerce ওয়েবসাইট যেখানে:
- ✅ Customer-রা product দেখতে ও কিনতে পারে
- ✅ bKash, Nagad, Rocket, Card দিয়ে payment করতে পারে  
- ✅ AI chatbot customer-দের সাহায্য করে
- ✅ Smart search দিয়ে product খুঁজে পাওয়া যায়
- ✅ Related product recommend করে

---

## 📂 মূল ফিচারসমূহ (Main Features)

### 1. 🏠 হোমপেজ ও পেজসমূহ (Core Pages)

| কাজ | বিবরণ |
|-----|-------|
| **Homepage** | Featured products ও categories দেখায় |
| **About Page** | Company সম্পর্কে তথ্য |
| **Contact Page** | Customer message পাঠাতে পারে |

---

### 2. 🏪 Product Management (Store)

| কাজ | বিবরণ |
|-----|-------|
| **Products** | সব product-এর নাম, দাম, ছবি, description |
| **Categories** | Computer, Headphones, Electronics ইত্যাদি |
| **Variants** | একই product-এর বিভিন্ন color/size |
| **Stock** | প্রতিটি product কতটা available আছে track করে |

**Admin Panel থেকে Product যোগ/Edit করা যায়**

---

### 3. 🛒 Shopping Cart (Cart)

| কাজ | বিবরণ |
|-----|-------|
| **Add to Cart** | Customer "Add to Cart" click করলে cart-এ যায় |
| **Update Quantity** | +/- দিয়ে quantity বাড়ানো/কমানো |
| **Remove Item** | Cart থেকে product সরানো |
| **Checkout** | Payment-এ যাওয়া |

---

### 4. 💳 Payment System

#### Supported Payment Methods:

| Method | Type |
|--------|------|
| **bKash** | মোবাইল ব্যাংকিং (Bangladesh) |
| **Nagad** | মোবাইল ব্যাংকিং (Bangladesh) |
| **Rocket** | মোবাইল ব্যাংকিং (Bangladesh) |
| **Stripe** | International Card Payment |

#### Payment Flow:
```
Checkout → Select Payment → Pay → Success Page → Order Created
```

**বিশেষ:** bKash sandbox কাজ না করলে Mock Gateway ব্যবহার করা যায় testing-এর জন্য।

---

### 5. 📋 Order Management

| Status | মানে |
|--------|------|
| **Ordered** | Order হয়েছে, payment complete |
| **Shipped** | Product পাঠানো হয়েছে |
| **Arrived** | Customer পেয়েছে |
| **Canceled** | Order বাতিল |

**Admin Panel থেকে Order status update করা যায়**

---

### 6. 🎫 Coupon/Discount System

| কাজ | বিবরণ |
|-----|-------|
| **Coupon Code** | যেমন: "SAVE10" দিলে 10% discount |
| **Usage Limit** | কতবার use করা যাবে সেট করা যায় |
| **Auto Deactivate** | Limit শেষ হলে automatic বন্ধ হয়ে যায় |

---

### 7. 👤 User Account

| কাজ | বিবরণ |
|-----|-------|
| **Sign Up** | নতুন account তৈরি |
| **Login** | Email/password দিয়ে login |
| **My Account** | Order history দেখা |
| **Saved Address** | Shipping address save করা যায় |

**বোনাস:** Guest হিসেবে order করলে, পরে sign up করলে সেই orders automatic account-এ link হয়ে যায়।

---

### 8. 🔍 Smart Search (AI-Powered)

| ফিচার | বিবরণ |
|-------|-------|
| **Semantic Search** | "gaming headphone" লিখলে related সব product দেখায় |
| **Autocomplete** | টাইপ করতে করতে suggestion দেয় |
| **Category Filter** | নির্দিষ্ট category-তে search |

**এটা সাধারণ keyword search না, AI বুঝে কী চাইছেন।**

---

### 9. ⭐ Product Recommendations

| কাজ | বিবরণ |
|-----|-------|
| **Similar Products** | Product page-এ related products দেখায় |
| **Based on Category** | Same category-র products suggest করে |
| **Based on Behavior** | Customer কী দেখেছে তার উপর ভিত্তি করে |

---

### 10. 🤖 AI Chatbot

| কাজ | বিবরণ |
|-----|-------|
| **Product Questions** | "laptop আছে?" জিজ্ঞেস করলে products দেখায় |
| **Order Status** | "আমার order কোথায়?" জিজ্ঞেস করলে status দেয় |
| **Coupon Info** | Discount সম্পর্কে জানতে চাইলে বলে দেয় |
| **24/7 Available** | সবসময় customer-দের সাহায্য করতে পারে |

---

## 🛡️ Security Features

- ✅ Secure payment (card info store হয় না)
- ✅ Password encrypted
- ✅ CSRF protection (hacking থেকে সুরক্ষা)
- ✅ HTTPS support

---

## 📱 Admin Panel

`/admin/` URL-এ যেতে হবে। Admin panel থেকে:
- Products add/edit/delete
- Categories manage
- Orders দেখা ও status update
- Coupons তৈরি
- Customer messages দেখা

---

## 💰 Payment Gateway Setup

| Gateway | কী লাগবে |
|---------|---------|
| **Stripe** | API Key (settings.py তে) |
| **bKash** | App Key, App Secret, Username, Password |

---

## 🚀 Server চালু করতে

```
python manage.py runserver
```

Browser-এ যান: `http://127.0.0.1:8000`

---

## 📞 সাপোর্ট

কোনো সমস্যা হলে developer-এর সাথে যোগাযোগ করুন।

---

*এই documentation তৈরি করা হয়েছে ShopSense e-commerce platform বোঝার জন্য।*
