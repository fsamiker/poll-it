<script>
import { Doughnut } from 'vue-chartjs'

export default {
    extends: Doughnut,
    props: ['chartData'],
    data() {
        return {
            options: {
                responsive: true,
                maintainAspectRatio: true
            }
        }
    },
    computed: {
        colors: function() {
            return ['#f9ec75', '#72dff6', '#c8f479', '#f9d379', '#f98c71']
        },
        renderData: function() {
            if(!this.chartData) {
                return {
                    labels: [],
                    datasets: []
                }
            }
            return {
                labels: this.chartData.labels,
                datasets: [{
                    label:'What is this?',
                    backgroundColor: this.colors,
                    data: this.chartData.data
                }]
            }
        }
    },
    mounted() {
        this.renderChart(this.renderData, this.options)
    },
};
</script>

<style scoped>

</style>