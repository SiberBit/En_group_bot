<template>
  <div>
    <h1>Чат боты</h1>
    <div v-if="status==='loading'" class="loading">
      <Loading/>
    </div>

    <div v-else-if="status==='success'">

      <button class="btn btn-outline" style="padding: 0" @click="add_chat_bot()">
        <div style="padding: 6px 12px; outline: none;" v-b-modal.modal-prevent-closing>
          Добавить чат-бота
        </div>
      </button>


      <!--Информация о чат боте-->
      <div class="chat-bots-list">
        <b-card v-for="chat_bot in chat_bots" v-bind:key=chat_bot.id
                style="padding: 10px">
          <h4 @click="set_chat_bot(chat_bot)">{{ chat_bot.name }}</h4>
          <div>
          </div>

          <div class="row">
            <div class="col-md-10">
              <p class="chat-bot-platform">
                <b>Платформа:</b>
                {{ chat_bot.platform }}
              </p>
              <p class="chat-bot-description">
                <b>Описание:</b>
                <br>
                {{ chat_bot.description }}
              </p>
              <p class="chat-bot-department">
                <b>Подразделение:</b>
                <br>
                {{ chat_bot.department.name }}
              </p>


              <!--Кнопка для раскрытия информации о API_URL и TOKEN-->
              <b-button class="collapse-btn" v-b-toggle="'collapse-' + chat_bot.id" style="padding: 0; outline: none;"
                        variant="link">
                Данные для API ↓
              </b-button>

              <!--Информация о API_URL и TOKEN-->
              <b-collapse :id="'collapse-' + chat_bot.id" class="mt-2">
                <b-card>
                  <div class="chat-bot-API_url">API_url: {{ chat_bot.API_url }}</div>
                  <div class="chat-bot-organization_slug">organization_slug: {{ organization.slug }}</div>
                  <div class="chat-bot-department_slug">department_slug: {{ chat_bot.department.slug }}</div>
                  <div class="chat-bot-token">TOKEN: {{ chat_bot.token }}</div>
                </b-card>
              </b-collapse>


            </div>
            <div class="col-md-2">
              <button class="btn btn-outline" style="padding: 0" @click="edit_chat_bot(chat_bot)">
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
                v-model="$data._editable_chat_bot.name"
                :state="validState"
                required
            ></b-form-input>
          </b-form-group>

          <!--Платформа-->
          <b-form-group
              :state="validState"
              label="Платформа"
              label-for="platform-input"
              invalid-feedback="Поле не может быть пустым"
          >
            <b-form-input
                id="platform-input"
                v-model="$data._editable_chat_bot.platform"
                :state="validState"
                required
            ></b-form-input>
          </b-form-group>


          <!--Описание-->
          <b-form-group
              :state="validState"
              label="Описание"
              label-for="description-input"
              invalid-feedback="Поле не может быть пустым"
          >

            <b-form-textarea
                id="description-input"
                v-model="$data._editable_chat_bot.description"
                :state="validState"
                required
                rows="4"
                max-rows="8"
            ></b-form-textarea>
          </b-form-group>


          <!--Подразделение-->
          <b-form-group id="input-group-3" label="Подразделение" label-for="visibility-input">
            <b-form-select
                id="visibility-input"
                v-model="$data._editable_chat_bot.department"
                required
            >
              <option v-for="department in departments" v-bind:value="department.id">
                {{ department.name }}
              </option>

            </b-form-select>
          </b-form-group>

        </form>
      </b-modal>
    </div>
  </div>
</template>

<script>
import Loading from "@/components/Loading";
import axios from "axios";

export default {
  name: "ChatBots",
  components: {
    Loading,
  },
  computed: {
    organization: {
      get() {
        return this.$store.getters.organization
      }
    },

  },
  data: function () {
    return {
      status: "loading",
      url: {
        chat_bot_api: this.$store.state.api_url + 'chat-bots/',
        edit_chat_bot_api: this.$store.state.api_url + 'chat-bot/',
        department_api: this.$store.state.api_url + 'departments/',
      },
      chat_bots: [],
      departments: [],


      form_action: '',
      form_name: '',
      _editable_chat_bot: {},
      validState: null,
    }
  },
  created: function () {
    this.get_chat_bots()
    this.get_departments()
  },
  methods: {
    get_chat_bots() {
      //получение списка подразделений
      this.status = "loading"
      axios.get(this.url.chat_bot_api + this.organization.slug + '/').then((response) => {
        console.log(response.data);
        const chat_bots = response.data;
        this.chat_bots = chat_bots.reverse();
        this.status = "success"
      });
    },
    get_departments() {
      //получение списка подразделений
      axios.get(this.url.department_api + this.organization.slug + '/').then((response) => {
        console.log(response.data);
        const departments = response.data;
        this.departments = departments.reverse();
        this.departments_list = departments.reverse();
      });
    },


    edit_chat_bot(chat_bot) {
      // сохранение редактируемого подразделения
      this.get_departments()
      this.form_name = 'Редактирование'
      this.form_action = 'edit'
      chat_bot.API_url = this.$store.state.api_url
      this.$data._editable_chat_bot = chat_bot
    },

    add_chat_bot() {
      // добавление нового подразделения
      this.get_departments()
      this.form_name = 'Добавление нового чат бота'
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
      this.$data._editable_chat_bot = {}
      this.validState = null
      this.form_action = ''
      this.form_name = ''
    },

    handleCancel() {
      // при закрытии формы
      this.status = "loading"
      //загружаем актуальную информацию
      this.get_chat_bots()
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
      let data = this.$data._editable_chat_bot
      const id = this.$data._editable_chat_bot.id
      delete data["id"]
      axios.put(this.url.edit_chat_bot_api + this.organization.slug + '/' + id + '/', data).then((response) => {
        console.log(response.data);
      }).catch((error) => {
        console.log(error);
      });
    },

    sendDataAdd() {
      let data = this.$data._editable_chat_bot
      data["organization"] = this.organization.id
      data["API_url"] = this.$store.state.api_url
      axios.post(this.url.edit_chat_bot_api + this.organization.slug + '/', data).then((response) => {
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
    },

  },


  watch: {
    organization: function () {
      this.get_chat_bots()
    }
  }
}
</script>

<style scoped>
.chat-bots-list {
  padding-top: 20px;
}

.collapse-btn {
  color: #ff941a;
}

.collapse-btn:hover,
.collapse-btn:active,
.collapse-btn:focus,
.collapse-btn:visited {
  -webkit-box-shadow: none;
  text-decoration: none;
  color: #ff941a;
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
</style>