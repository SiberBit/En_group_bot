<template>
  <div>
    <h1>Подразделения</h1>
    <div v-if="status==='loading'" class="loading">
      <Loading/>
    </div>

    <div v-else-if="status==='success'">

      <button class="btn btn-outline" style="padding: 0" v-if="user.is_staff" @click="add_department()">
        <div style="padding: 6px 12px; outline: none;" v-b-modal.modal-prevent-closing>
          Добавить подразделение
        </div>
      </button>


      <div class="department-list ">
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
              <div v-if="department.chat_bot.length === 0" class="chat-bots">
                Чат боты не добавлены
              </div>
              <div v-else class="chat-bots">
                <div class="chat-bots-title">
                  Чат боты:
                </div>
                <li v-for="chat_bot in department.chat_bot">
                  <a class="chat-bot-name" @click="chat_bot_info(chat_bot)">
                    <div style="outline: none; display: inline-block" v-b-modal.modal-chat-bot>
                      {{ chat_bot.name }} ({{ chat_bot.platform }})
                    </div>
                  </a>

                  <br>
                </li>

              </div>
            </div>
            <div class="col-md-2" v-if="user.is_staff">
              <button class="btn btn-outline" style="padding: 0" @click="edit_department(department)">
                <div style="padding: 6px 12px; outline: none;" v-b-modal.modal-prevent-closing>
                  Редактировать
                </div>
              </button>
            </div>
          </div>

        </b-card>
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
          ok-variant="outline-success"
          cancel-title="Отмена"
          cancel-variant="outline-secondary"
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


      <!--Модальное окно Информация о боте-->
      <b-modal
          id="modal-chat-bot"
          ref="modal"
          :title="chat_bot.name"
          @show="resetModalChatBot"
          @hidden="handleCancelChatBot"
          ok-only
      >

        <div chat-bot-info>
          <p class="chat-bot-platform">
            <b>Платформа:</b>
            {{ chat_bot.platform }}
          </p>
          <p class="chat-bot-description">
            <b>Описание:</b>
            <br>
            {{ chat_bot.description }}
          </p>


          <!--Кнопка для раскрытия информации о API_URL и TOKEN-->
          <b-button class="collapse-btn" v-b-toggle="'collapse-' + chat_bot.id" style="padding: 0; outline: none;"
                    variant="link">
            Данные для API ↓
          </b-button>

          <!--Информация о API_URL и TOKEN-->
          <b-collapse :id="'collapse-' + chat_bot.id" class="mt-2">
            <b-card>
              <div class="chat-bot-API_url"><b>API_url:</b> {{ chat_bot.API_url }}</div>
              <div class="chat-bot-organization_slug"><b>organization_slug:</b> {{ organization.slug }}</div>
              <div class="chat-bot-department_slug"><b>department_slug:</b> {{ department.slug }}</div>
              <div class="chat-bot-token"><b>TOKEN:</b> {{ chat_bot.token }}</div>
            </b-card>
          </b-collapse>
        </div>
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
    user() {
      return this.$store.getters.user
    },
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
      form_name: '',
      _editable_department: {},
      validState: null,

      chat_bot: {},
      department: {},


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
      this.form_name = 'Редактирование'
      this.form_action = 'edit'
      this.$data._editable_department = department
    },

    add_department() {
      // добавление нового подразделения
      this.form_name = 'Добавление нового подразделения'
      this.form_action = 'add'

    },

    checkFormValidity() {
      // проверка валидности формы
      const valid = this.$refs.form.checkValidity()
      this.validState = valid
      return valid
    },

    resetModal() {
      // сброс формы
      this.$data._editable_department = {}
      this.validState = null
      this.form_action = ''
      this.form_name = ''
    },

    handleCancel() {
      // при закрытии формы
      this.status = "loading"
      //загружаем актуальную информацию
      this.get_departments()
      this.resetModal()
    },


    resetModalChatBot() {
      this.chat_bot = {}
    },
    handleCancelChatBot() {
      this.chat_bot = {}
    },


    chat_bot_info(chat_bot) {
      this.chat_bot = chat_bot
      this.department = chat_bot.department
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
      //const slug = Slug(this.$data._editable_department.name)
      //data["slug"] = slug
      delete data["id"]
      axios.put(this.url.edit_department_api + id + '/', data).then((response) => {
        console.log(response.data);
      }).catch((error) => {
        console.log(error);
      });
    },

    sendDataAdd() {
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
      this.get_departments()
    }
  },
}
</script>

<style scoped>
.department-list {
  padding-top: 20px;
}

a {
  color: #393330;
}

a:hover {
  color: #ff941a;
  text-decoration: underline;
}

/*Модальное окно*/
.modal-footer {
  background-color: blue;
}


/*Кнопки*/
.btn-outline {
  color: #ff941a;
  border-color: #ff941a;
}

.btn-outline:hover,
.btn-outline:focus,
.btn-outline:visited,
.btn-outline:active {
  background-color: #ff941a;
  border-color: #ff941a;
  color: white;
}

/*Карточки*/
.card {
  border: 1px solid rgb(255, 148, 26);
  margin-bottom: 10px;
}

h1 {
  margin: 10px 0 20px;
}

/*Чат бот*/
.chat-bot-name:hover {
  color: #ff941a;
  text-decoration: underline;
}
</style>