
const productapp = Vue.createApp({
    delimiters: ['[[', ']]'],
    store: store,
    computed: {
        totalQuantity() {
            return this.products.reduce((sum, p) => sum + p.quantity, 0);
        },
        totalCost() {
            return this.products.reduce((sum, p) => sum + p.total_cost, 0);
        }
    },
    data() {
        return {
            first_name: '',
            last_name: '',
            email: '',
            address: '',
            zipcode: '',
            place: '',
            products: {{ products_json|safe }}
        }
    },
    methods: {
        buy() {
            var stripe = Stripe('{{ pub_key }}');
            fetch("/api/create_checkout_session/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                credentials: 'same-origin',
            })
            .then(response => response.json())
            .then(session => stripe.redirectToCheckout({ sessionId: session.id }))
            .then(result => { if(result.error){ alert(result.error.message) } })
            .catch(error => console.log("Error:", error));
        },
        submitForm() {

        var data = {
            first_name: this.first_name,
            last_name: this.last_name,
            email: this.email,
            address: this.address,
            zipcode: this.zipcode,
            place: this.place
        };

        console.log(data);

        alert("Submit clicked!");
        fetch('/api/checkout/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}'
    },
    credentials: 'same-origin',
    body: JSON.stringify(data)
})
.then(res => res.json())
.then(data => {
    if (data.success) {
        window.location.href = `/order/success/${data.order_id}/`;
    } else {
        alert("Checkout failed!");
    }
})
.catch(error => console.error('Error:', error));

    },

        incrementQuantity(product_id, quantity){
            const data = {
            product_id: product_id,
            update: true,
            quantity: quantity + 1
        }
        this.$store.commit('increment', 1)

        fetch('/api/add_to_cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            credentials: 'same-origin',
            body: JSON.stringify(data)
        })
        .then(response => {
            this.products = this.products.map(product => {
                if (product.id === product_id) {
                    return { 
                        ...product, 
                        quantity: product.quantity + 1, 
                        total_cost: (product.quantity + 1) * product.price 
                    };
                }
            return product;
            })
        })
        .catch(error => console.error('Error:', error))
        },

        decrementQuantity(product_id, quantity){
            const data = {
                product_id: product_id,
                update: true,
                quantity: quantity - 1
            }

            fetch('/api/add_to_cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                credentials: 'same-origin',
                body: JSON.stringify(data)
            })
            .then(response => {
                this.products = this.products.map(product => {
                    if (product.id === product_id) {
                        const newQuantity = product.quantity - 1;
                        if (newQuantity <= 0) {
                            // remove the product from products array
                            this.$store.commit('decrement', product.quantity); // decrement by the full quantity removed
                            return null;
                        }
                        return { 
                            ...product, 
                            quantity: newQuantity,
                            total_cost: newQuantity * product.price
                        };
                    }
                    return product;
                }).filter(Boolean); // remove nulls
                // if product was removed, cart count already updated above
                if (quantity === 1) {
                    // already removed, nothing else needed
                } else {
                    this.$store.commit('decrement', 1);
                }
            })
            .catch(error => console.error('Error:', error))
        },


        removeFromCart(product_id) {
            const product = this.products.find(p => p.id === product_id)
            if (!product) return;

            var data = { 'product_id': product_id }

            fetch('/api/remove_from_cart/', {   
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'   
                },
                credentials: 'same-origin',  
                body: JSON.stringify(data)   
            })
            .then(response => {
                console.log(response)
                // Remove product from local array
                this.products = this.products.filter(p => p.id !== product_id)
                
                // Update Vuex store count
                if (this.products.length === 0) {
                    this.$store.commit('setCount', 0) // set to 0 explicitly
                } else {
                    this.$store.commit('decrement', product.quantity)
                }
            })
            .catch(error => {
                console.error('Error:', error)
            })
        }   

    }
})
productapp.use(store)
productapp.mount("#cartapp")
