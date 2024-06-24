const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))


Vue.component("keyboardwrapper", {
    template: '#keyboardwrapper',
    data () {
      return {
        active: null,
        show: false,
        NUM: '',
        
        result: []
      };
    },
    computed: {
      // 统计打中的地鼠数量
      num: function () {
        return this.result.join('');
      }
    },
    created () {
    },
    mounted () {
    },
    methods: {
      msDown (v) {
        this.active = v;
      },
      msUp (v) {
        this.active = '';
      },
      stopInput () {
        return false;
      },
      change (val, $event) {
        console.log(val, $event)
        if (this.result.length === 0 && val === '.') {
          return false;
        } else {
          this.result.push(val);
          this.NUM = this.result.join('');
        }
      },
      del () {
        this.result.pop();
        this.NUM = this.result.join('');
        this.$emit('del', this.NUM);
      },
      comfirm () {
        this.$emit('comfirm', this.NUM);
        this.show = false;
      }
    }
  })
  new Vue( ).$mount('#app')
