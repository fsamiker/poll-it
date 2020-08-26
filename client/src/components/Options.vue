<template>
    <div class="field has-addons">
        <div class="control is-expanded">
            <div class="select is-fullwidth">
            <select v-model="votedOption" name="options">
                <option disabled value='' >Select An Option</option>
                <option v-for="option in optionList" :key="option.id" :value="option.id">{{ option.body }}</option>
            </select>
            </div>
        </div>
    <div class="control">
        <VoteButton :disabled="!expired" :optionId="votedOption" :hasVoted="voted" :pollId="pollId"></VoteButton>
    </div>
</div>
</template>

<script>
import VoteButton from './VoteButton'

export default {
  name: 'Options',
  props: ['optionList', 'pollId', 'expired'],
  components: {
      VoteButton
    },
  data: function() {
      return {
          'votedOption': ''
      }
  },
  computed: {
      voted: function() {
          if (Object.keys(this.$store.state.votedPolls).includes(this.pollId.toString())) {
              return true;
          }
          return false;
      },
  }
};
</script>

<style scoped>
</style>