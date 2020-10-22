let categories = JSON.parse(document.getElementById('djangoData').textContent);


new Vue({
    el: '#app',
    data: {
        url: {
            categories_api: '/api/categories/',
        },
        categories: [],
        category: {}
    },
    created: function () {
        this.categories = categories;
    },
    methods: {
        get_categories(category) {
            // получаем подкатегории
            axios.get(this.url.categories_api + category.id).then((response) => {
                console.log(response.data);
                categories = response.data;
                this.categories = categories;
                this.category = category
            });
        },

        get_start_categories() {
            // получаем начальные категории
            axios.get(this.url.categories_api).then((response) => {
                console.log(response.data);
                categories = response.data;
                this.categories = categories;
                this.category = {};
            });
        },
    }


})