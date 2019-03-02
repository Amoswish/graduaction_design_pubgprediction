new Vue({
    el: '#app',
    data: {
      screenwidth:100,
      screenheight:100,
        options: [
            'Option 1', 'Option 2', 'Option 3', 'Option 4',
            'Option 5', 'Option 6', 'Option 7', 'Option 8',
            'Option 9', 'Option 10'
            ],
        labelPosition: 'top',
        form: {
            input: '',
            select: '',
            date: '',
            radio: '',
            checkbox: [],
            switch: false,
            slider: 30,
            textarea: ''
        },
        shift: 'input_data',
        sort: {
            name: '',
            order: 'asc'
          },
        columns: [
              { title: 'Dessert (100g serving)', width: 200, name: 'name' },
              { title: 'Calories', name: 'calories', width: 126, align: 'center', sortable: true },
              { title: 'Fat (g)', name: 'fat', width: 126, align: 'center', sortable: true },
              { title: 'Carbs (g)', name: 'carbs', width: 126, align: 'center', sortable: true },
              { title: 'Protein (g)', name: 'protein', width: 126, align: 'center', sortable: true },
              { title: 'Iron (%)', name: 'iron', width: 126, align: 'center', sortable: true }
          ],
        list: [
            {
                name: 'Frozen Yogurt',
                calories: 159,
                fat: 6.0,
                carbs: 24,
                protein: 4.0,
                iron: 1
              },
              {
                name: 'Ice cream sandwich',
                calories: 237,
                fat: 9.0,
                carbs: 37,
                protein: 4.3,
                iron: 1
              },
              {
                name: 'Eclair',
                calories: 262,
                fat: 16.0,
                carbs: 23,
                protein: 6.0,
                iron: 7
              },
              {
                name: 'Cupcake',
                calories: 305,
                fat: 3.7,
                carbs: 67,
                protein: 4.3,
                iron: 8
              },
              {
                name: 'Gingerbread',
                calories: 356,
                fat: 16.0,
                carbs: 49,
                protein: 3.9,
                iron: 16
              },
              {
                name: 'Jelly bean',
                calories: 375,
                fat: 0.0,
                carbs: 94,
                protein: 0.0,
                iron: 0
              },
              {
                name: 'Lollipop',
                calories: 392,
                fat: 0.2,
                carbs: 98,
                protein: 0,
                iron: 2
              },
          ],
        },
        computed:{
          widthchange:function(){
              return this.screenwidth;
          },
          heightchange:function(){
              return this.screenheight;
          },
        },
        mounted () {
          //适配主页背景图片格式
          this.screenwidth = window.innerWidth;
          this.screenheight = window.innerHeight;
          console.log(this.screenheight);
          
        },
        methods: {
        handleSortChange ({name, order}) {
            this.list = this.list.sort((a, b) => order === 'asc' ? a[name] - b[name] : b[name] - a[name]);
        },
        resize () {
          this.screenwidth = window.innerWidth;
          this.screenheight = window.innerHeight;
          if(this.screenwidth/this.screenheight>1){
              this.backgroundimg = "../../static/res/backgroundimg/backgroundimgwidth.jpeg"
          }
          else{
              this.backgroundimg = '../../static/res/backgroundimg/backgroudimgheight.jpg'
          }
      },

    },
    watch: {
    },
});