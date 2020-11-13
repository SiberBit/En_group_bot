<template>
  <div>
    <h1>Подразделения</h1>
    <div v-if="status==='loading'" class="loading">
      <Loading/>
    </div>

    <div v-else-if="status==='success'">

      <b-button style="padding: 0" @click="add_department()" variant="outline-primary">
        <div style="padding: 6px 12px; outline: none;" v-b-modal.modal-prevent-closing>
          Добавить подразделение
        </div>
      </b-button>


      <div class="department-list">
        <b-card v-for="department in departments" v-bind:key=department.id
                style="padding: 10px">
          <router-link to="/categories/">
            <h4 @click="set_department(department)">{{ department.name }}</h4>
          </router-link>
          <div>
            Использование:
            <p v-if="department.visibility">Для клиентов</p>
            <p v-else>Внутри организации</p>
          </div>
          <!--Информация о чат боте-->
          <div class="row">
            <div class="col-md-10">
              <a href="">(Информация о боте)</a>
            </div>
            <div class="col-md-2">
              <b-button style="padding: 0" @click="edit_department(department)" variant="outline-primary">
                <div style="padding: 6px 12px; outline: none;" v-b-modal.modal-prevent-closing>
                  Редактировать
                </div>
              </b-button>
            </div>
          </div>

        </b-card>
      </div>

      <!--Модальное окно редактирования-->
      <b-modal
          id="modal-prevent-closing"
          ref="modal"
          title="Редактирование"
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
                v-model="$data._editable_department.name"
                :state="validState"
                required
            ></b-form-input>


            <!--Использование-->
            <b-form-group id="input-group-3" label="Использование:" label-for="visibility-input">
              <b-form-select
                  id="visibility-input"
                  v-model="$data._editable_department.visibility"
                  :options="[
                              {value:false, text:'Внутри организации'},
                              {value:true, text:'Для клиентов'}
                            ]"


                  required
              ></b-form-select>
            </b-form-group>


          </b-form-group>
        </form>
      </b-modal>
    </div>
  </div>


</template>

<script>

import Loading from "@/components/Loading";
import axios from 'axios'


export default {
  name: "Department",
  components: {
    Loading
  },
  computed: {
    organization: {
      get() {
        return this.$store.getters.organization
      },
    },

  },
  data: function () {
    return {
      status: "loading",
      url: {
        department_api: this.$store.state.api_url + 'departments/',
        edit_department_api: this.$store.state.api_url + 'department/',
      },
      departments: [],

      form_action: '',
      _editable_department: {},
      validState: null,

    }
  },
  created: function () {
    this.get_departments()
  },

  methods: {
    get_departments() {
      //получение списка подразделений
      this.status = "loading"
      axios.get(this.url.department_api + this.organization.slug + '/').then((response) => {
        console.log(response.data);
        const departments = response.data;
        this.departments = departments.reverse();
        this.status = "success"
      });
    },
    set_department(department) {
      // сохранение выбранного подразделения
      this.$store.commit('set_department', department)
    },


    edit_department(department) {
      // сохранение редактируемого подразделения

      this.form_action = 'edit'
      this.$data._editable_department = department
    },

    add_department() {
      // добавление нового подразделения

      this.form_action = 'add'

    },

    checkFormValidity() {
      // проверка валидности формы
      const valid = this.$refs.form.checkValidity()
      console.log(valid)
      this.validState = valid
      return valid
    },

    resetModal() {
      // сброс формы
      this.$data._editable_department = {}
      this.validState = null
      this.form_action = ''
    },

    handleCancel() {
      // при закрытии формы
      this.status = "loading"
      //загружаем актуальную информацию
      this.get_departments()
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
      // отправляем данные на сервер
      let data = this.$data._editable_department
      const id = this.$data._editable_department.id
      const slug = Slug(this.$data._editable_department.name)
      data["slug"] = slug
      delete data["id"]
      axios.put(this.url.edit_department_api + id + '/', data).then((response) => {
        console.log(response.data);
      }).catch((error) => {
        console.log(error);
      });
    },

    sendDataAdd(){
      let data = this.$data._editable_department
      const slug = Slug(this.$data._editable_department.name)
      data["slug"] = slug
      data["organization"] = this.organization.id

      axios.post(this.url.edit_department_api, data).then((response) => {
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
      }
      else if(this.form_action === 'add')
      {
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
      this.get_departments()
    }
  },
}
</script>

<style scoped>
.department-list {
  padding-top: 20px;
}
</style>