<template>
    <button class="button delete-poll is-primary" 
    :class="{ 'is-loading': isLoading }"
    @click="remove">
        <span class="icon is-small">
            <i class="far fa-trash-alt"></i>
        </span>
    </button>
</template>

<script>
import { deletePoll } from '@/api'

export default {
  name: 'DeletePollButton',
  props: ['pollId'],
  data: function() {
      return {
          isLoading: false,
          message: ''
      }
  },
  methods:{
      remove: function() {
          deletePoll(this.$store.getters.getAuthHeader, this.pollId)
          .then(() => {
              console.log('successfully deleted');
              this.$emit('remove')
          });
      }
  }
};
</script>

<style scoped>
</style>