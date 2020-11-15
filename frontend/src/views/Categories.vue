<template>

  <div>
    <h1>Категории</h1>
    <h3>{{ department.name }}</h3>

    <div v-if="status==='loading'" class="loading">
      <Loading/>
    </div>

    <div v-else-if="status==='success'">


      <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
          <li class="breadcrumb-item" aria-current="page" @click="get_start_categories">
            <a v-if="category_menu.length!==0" href="#">
              В начало
            </a>
            <a v-else>
              В начало
            </a>
          </li>
          <li v-for="category in category_menu"
              v-bind:key=category.id
              @click="get_categories(category)"
              class="breadcrumb-item "
          >
            <a v-if="category !== category_menu[category_menu.length-1]" href="#">
              {{ category.name }}
            </a>
            <a v-else>
              {{ category.name }}
            </a>
          </li>
        </ol>
      </nav>


      <div class="row">

        <div v-for="category in categories" v-bind:key=category.id style="padding: 5px">
          <b-button variant="success">
            <div class="row" style="margin: 0 5px; ">
              <div style="padding-right: 10px" @click="get_categories(category)">
                {{ category.name }}
              </div>
              <div title="Редактировать" style="" @click="edit_category(category)" variant="outline-primary">
                <div style="outline: none;" v-b-modal.modal-prevent-closing>
                  <img style="height: 20px" src="../assets/text_edit.png">
                </div>
              </div>
            </div>
          </b-button>
        </div>

        <!--Кнопка Добавить категорию-->

        <div v-if="!parent_category || parent_category.target==='categories'" style="padding: 5px">
          <b-button title="Добавить категорию" style="padding: 0" @click="add_category()" variant="outline-success">
            <div style="padding: 6px 12px; outline: none;" v-b-modal.modal-prevent-closing>
              <img style="height: 20px" src="../assets/plus.svg">
            </div>
          </b-button>
        </div>

        <div v-else>
          <Questions :category_id="parent_category.id"/>
        </div>


      </div>
    </div>


    <!--Модальное окно редактирования-->
    <b-modal
        id="modal-prevent-closing"
        ref="modal"
        :title="form_name"
        @show="resetModal"
        @hidden="handleCancel"
        @ok="handleOk"
        ok-title="Сохранить"
        cancel-title="Отмена"
    >

      <!--Форма редактирования-->
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <!--Название-->
        <b-form-group
            :state="validState"
            label="Название"
            label-for="name-input"
            invalid-feedback="Поле не может быть пустым"
        >
          <b-form-input
              id="name-input"
              v-model="$data._editable_category.name"
              :state="validState"
              required
          ></b-form-input>


          <!--Использование-->
          <b-form-group id="input-group-3" label="Что будет содержать:" label-for="visibility-input">
            <b-form-select
                id="visibility-input"
                v-model="$data._editable_category.target"
                :options="[
                              {value:'categories', text:'Подкатегории'},
                              {value:'questions', text:'Вопросы'}
                            ]"


                required
            ></b-form-select>
          </b-form-group>


        </b-form-group>
      </form>
    </b-modal>


  </div>
</template>

<script>
import axios from 'axios'
import Loading from "@/components/Loading";
import Questions from "@/components/Questions";

export default {
  name: "Categories",
  components: {
    Loading,
    Questions
  },
  data: function () {
    return {
      status: "loading",
      url: {
        categories_api: this.$store.state.api_url + 'categories/',
        edit_category_api: this.$store.state.api_url + 'category/',
      },
      categories: [],
      parent_category: null,

      form_action: '',
      form_name: '',
      _editable_category: {},
      validState: null,

      category_menu: [],
    }
  },

  computed: {
    organization: {
      get() {
        return this.$store.getters.organization
      },
    },
    department: {
      get() {
        return this.$store.getters.department
      },
    }
  },

  created: function () {

    this.get_start_categories();
  },
  methods: {
    get_categories(category) {

      if (!category) {
        this.get_start_categories()
      } else {

        // получаем подкатегории
        this.status = "loading"

        this.parent_category = category

        //Смотрим есть ли категория в меню
        if (this.category_menu.indexOf(category) !== -1) {
          this.category_menu.length = category.level - 1 // если есть, убираем категории стоящие выше по дереву
        }
        this.category_menu.push(category)// добавляем категорию в меню

        axios.get(this.url.categories_api + this.organization.slug + '/' + this.department.slug + '/' + category.id + '/').then((response) => {
          console.log(response.data);
          const categories = response.data;
          this.status = "success"
          this.categories = categories;
        });
      }
    },
    get_start_categories() { // получаем начальные категории

      this.category_menu = []

      this.status = "loading"
      axios.get(this.url.categories_api + this.organization.slug + '/' + this.department.slug + '/').then((response) => {
        console.log(response.data);
        const categories = response.data;
        this.categories = categories;
        this.parent_category = null;
        this.status = "success"
      });
    },

    add_category() {
      this.form_name = 'Добавление категории'
      this.form_action = 'add'
    },
    edit_category(category) {
      this.form_name = 'Редактирование'
      this.form_action = 'edit'
      this.$data._editable_category = category
    },

    checkFormValidity() {
      // проверка валидности формы
      const valid = this.$refs.form.checkValidity()
      this.validState = valid
      return valid
    },
    resetModal() {
      // сброс формы
      this.$data._editable_category = {}
      this.validState = null
      this.form_action = ''
      this.form_name = ''
    },
    handleCancel() {
      // при закрытии формы
      this.status = "loading"
      //загружаем актуальную информацию
      this.get_categories(this.parent_category)
      this.resetModal()
    },
    handleOk(bvModalEvt) {
      // при нажатии кнопки Сохранить

      // Prevent modal from closing
      bvModalEvt.preventDefault()
      // Trigger submit handler
      this.handleSubmit()
    },

    sendDataEdit() {
      //отправляем данные на сервер
      let data = this.$data._editable_category
      const id = this.$data._editable_category.id
      delete data["id"]
      axios.put(this.url.edit_category_api + this.organization.slug + '/' + this.department.slug + '/' + id + '/', data).then((response) => {
        console.log(response.data);
      }).catch((error) => {
        console.log(error);
      });
    },
    sendDataAdd() {
      let data = this.$data._editable_category


      if (this.parent_category) {
        data["level"] = this.parent_category.level + 1
        data["parent_id"] = this.parent_category.id
      } else {
        data["level"] = 1
        data["parent_id"] = 0
      }
      data["author"] = this.$store.getters.user.id
      data["department"] = this.department.id

      axios.post(this.url.edit_category_api + this.organization.slug + '/' + this.department.slug + '/', data).then((response) => {
        console.log(response.data);
      }).catch((error) => {
        console.log(error);
      });
    },
    handleSubmit() {
      //отправка формы

      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return
      }

      if (this.form_action === 'edit') {
        this.sendDataEdit()
      } else if (this.form_action === 'add') {
        this.sendDataAdd()
      }


      // Скрываем модальное окно
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing')
      })
    }
  },
  watch: {
    organization: function () {
      this.$router.push('/department')
    }
  },
}
</script>

<style scoped>
</style>