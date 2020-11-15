<template>
  <div class="question-list">

    <b-button style="padding: 0; margin-bottom: 15px" @click="add_question()" variant="outline-primary">
      <div style="padding: 6px 12px; outline: none;" v-b-modal.modal-prevent-closing-questions>
        Добавить вопрос
      </div>
    </b-button>


    <table class="table table-bordered">
      <thead>
      <tr>
        <th class="w-25" scope="col">Вопрос</th>
        <th class="w-75" scope="col">Ответ</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="question in questions" v-bind:key=question.id>
        <td>
          {{ question.question }}
        </td>
        <td>
          {{ question.answer }}
          <br>
          <div class="text-right">
            <b-button style="padding: 0" @click="edit_question(question)" variant="outline-primary">
              <div style="padding: 6px 12px; outline: none;" v-b-modal.modal-prevent-closing-questions>
                Редактировать
              </div>
            </b-button>
          </div>
        </td>
      </tr>
      </tbody>
    </table>


    <!--Модальное окно редактирования-->
    <b-modal
        id="modal-prevent-closing-questions"
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
        <!--Вопрос-->
        <b-form-group
            :state="validState"
            label="Вопрос"
            label-for="question-input"
            invalid-feedback="Поле не может быть пустым"
        >
          <b-form-textarea
              id="question-input"
              v-model="$data._editable_question.question"
              :state="validState"
              required
              rows="1"
              max-rows="3"
          ></b-form-textarea>
        </b-form-group>


        <!--Ответ-->
        <b-form-group
            :state="validState"
            label="Ответ"
            label-for="answer-input"
            invalid-feedback="Поле не может быть пустым"
        >
          <b-form-textarea
              id="answer-input"
              v-model="$data._editable_question.answer"
              :state="validState"
              required
              rows="4"
              max-rows="8"
          ></b-form-textarea>
        </b-form-group>

      </form>
    </b-modal>


  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Questions",
  props: ['category_id'],
  data: function () {
    return {
      status: "loading",
      url: {
        questions_api: this.$store.state.api_url + 'questions/',
        edit_questions_api: this.$store.state.api_url + 'question/',
      },
      questions: [],

      form_action: '',
      form_name: '',
      _editable_question: {},
      validState: null,

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
    this.get_questions();
  },
  methods: {
    get_questions() { // получаем вопросы
      this.status = "loading"
      axios.get(this.url.questions_api + this.organization.slug + '/' + this.department.slug + '/' + this.category_id + '/').then((response) => {
        console.log(response.data);
        const questions = response.data;
        this.questions = questions.reverse();
        this.status = "success"
      });
    },

    edit_question(question) {
      // сохранение редактируемого подразделения
      this.form_name = 'Редактирование'
      this.form_action = 'edit'
      this.$data._editable_question = question
    },

    add_question() {
      // добавление нового подразделения
      this.form_name = 'Добавление вопроса'
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
      this.$data._editable_question = {}
      this.validState = null
      this.form_action = ''
      this.form_name = ''
    },

    handleCancel() {
      // при закрытии формы
      this.status = "loading"
      //загружаем актуальную информацию
      this.get_questions()
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
      let data = this.$data._editable_question

      const id = this.$data._editable_question.id
      delete data["id"]
      data["category"] = this.category_id

      data["author"] = this.$store.getters.user.id
      axios.put(this.url.edit_questions_api + this.organization.slug + '/' + this.department.slug + '/' + id + '/', data).then((response) => {
        console.log(response.data);
      }).catch((error) => {
        console.log(error);
      });
    },

    sendDataAdd() {
      let data = this.$data._editable_question
      data["category"] = this.category_id
      data["author"] = this.$store.getters.user.id
      axios.post(this.url.edit_questions_api + this.organization.slug + '/' + this.department.slug + '/', data).then((response) => {
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
        this.$bvModal.hide('modal-prevent-closing-questions')
      })
    }
  }
}
</script>

<style scoped>

</style>