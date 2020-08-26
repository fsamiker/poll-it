<template>
  <div class="columns is-multiline mt-4">
    <Poll v-for="(poll, index) in polls" :key="poll.id" :pollData="poll"
      @remove="removePoll(index)"></Poll>
  </div>
</template>

<script>
// @ is an alias to /src
import Poll from "@/components/Poll.vue";
import { fetchPolls } from '@/api'

export default {
  name: "Polls",
  props: ['user_id'],
  data: function() {
    return {
      polls : [],
      pollPaginationLinks: '',
      metadata: ''
    }
  },
  components: {
    Poll
  },
  created: function() {
      this.getPolls();
  },
  methods: {
    getPolls: function() {
          fetchPolls(this.user_id)
          .then(response => response.json())
          .then(data => this.updatePolls(data));
      },
    updatePolls: function(pollResponse) {
      this.polls.push(...pollResponse.items);
      this.pollPaginationLinks = pollResponse._links;
      this.metadata = pollResponse._meta
    },
    pushPoll: function(pollInfo) {
      this.polls.unshift(pollInfo);
    },
    removePoll: function(index) {
      console.log(`remove ${index}`)
      this.polls.splice(index, 1)
    }
  }
};
</script>

<style scoped>
</style>
