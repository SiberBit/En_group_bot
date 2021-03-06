let categories = JSON.parse(document.getElementById('djangoData').textContent);


new Vue({
    el: '#app',
    data: {
        url: {
            categories_api: '/api/v1/categories/',
        },
        categories: [],
        category: []
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

                if (this.category[-1] != category){
                    this.category.push(category)
                }
                else{
                    this.category.pop()
                }
                console.log(this.category);
            });
        },

        get_start_categories() {
            // получаем начальные категории
            axios.get(this.url.categories_api).then((response) => {
                console.log(response.data);
                categories = response.data;
                this.categories = categories;
                this.category = [];
            });
        },
    }


})