<template>
    <div class="button-group">
        <button class="button vote is-primary" 
            :disabled="!optionId || hasVoted"
            v-show="!hasVoted"
            :class="{ 'is-loading': isLoading }"
            @click="vote">
            Vote
            </button>
        <button v-show="hasVoted" class="button is-danger is-outlined is-static level-item is-small">Voted</button>
    </div>
</template>

<script>
import { voteAsGuest, voteAsUser } from '@/api'

export default {
  name: 'VoteButton',
  props: ['optionId', 'hasVoted', 'pollId'],
  data: function() {
      return {
          isLoading: false,
          message: ''
      }
  },
  methods:{
      vote: function() {
          let voteResponse;
          this.isLoading = true;
          if(this.$store.state.user) {
              voteResponse = voteAsUser(this.$store.getters.getAuthHeader, this.optionId);
          }
          else {
              voteResponse = voteAsGuest(this.optionId);
          }
          voteResponse.then(response => response.json())
          .then(data => {
              this.message = data.message;
              this.isLoading = false;
              this.recordVoted();
              });
      },
      recordVoted: function() {
          this.$store.commit('updateVotedPolls', {[this.pollId]: this.optionId});
      }
  }
};
</script>

<style scoped>
</style>