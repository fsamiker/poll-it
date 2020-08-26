<template>
<div class="modal">
    <div class="modal-background"></div>
    <div class="modal-card">
        <header class="modal-card-head">
            <p class="modal-card-title has-text-centered">Create Poll</p>
            <button class="delete" aria-label="close" @click="close"></button>
        </header>
        <section class="modal-card-body">
            <div class="field">
                <label class="label">Question</label>
                <div class="control has-icons-left">
                    <input class="input" type="text" placeholder="What would you like to ask?" v-model="title">
                    <span class="icon is-small is-left">
                        <i class="fas fa-question"></i>
                    </span>
                </div>
            </div>
            <div class="field">
                <label class="label">Description</label>
                <div class="control has-icons-left">
                    <input class="input" type="text" placeholder="Context" v-model="description">
                    <span class="icon is-small is-left">
                        <i class="fas fa-align-justify"></i>
                    </span>
                </div>
                <p class="help">Additional description. Max 140 characters.</p>
            </div>
            <div class="options"
            v-for="(option, i) in options"
            :key="i">
                <div class="field has-addons mb-3">
                    <p class="control">
                        <a class="button is-static">
                        Option {{ i + 1 }}
                        </a>
                    </p>
                    <p class="control">
                        <input class="input" type="text" placeholder="New Option" v-model="option.body">
                    </p>
                    <p class="control">
                        <a class="button" @click="removeOption(i)">
                            <span class="icon is-small is-right is-info">
                                <i class="fas fa-times"></i>
                            </span>
                        </a>
                    </p>
                </div>
            </div>
            <div class="control">
                <button class="button is-primary" @click="addOption" v-show="numberOptions < 5">
                    <i class="fas fa-plus"></i>
                </button>
            </div>
        </section>
        <footer class="modal-card-foot is-grouped-centered">
            <button class="button is-primary" @click="submitPoll">Submit</button>
        </footer>
    </div>
</div>
</template>

<script>
import { createPoll } from '@/api'

export default {
  name: 'CreatePollForm',
  data: function() {
      return {
          title: '',
          description: '',
          options: [
              {
                  body: ''
              },
              {
                  body: ''
              }
          ]
      }
  },
  computed: {
      numberOptions: function() {
          return this.options.length
      }
  },
  methods: {
      addOption: function() {
          this.options.push(
            {
                body: ''
            }
          )
      },
      removeOption: function(index) {
          this.options.splice(index, 1);
      },
      submitPoll: function() {
          let payload = {
              'title': this.title,
              'description': this.description,
              'options': this.options
          }
          createPoll(this.$store.getters.getAuthHeader, payload)
          .then(response => response.json())
          .then(data => {
              console.log(data);
              this.$emit('update', data)
              this.close()
          })
      },
      clearForm: function() {
          this.title = ''
          this.description = ''
          this.options = [
              {
                  body: ''
              },
              {
                  body: ''
              }
          ]
      },
      close: function() {
          this.$emit('close');
      }
  }
};
</script>

<style scoped>
</style>