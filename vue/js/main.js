new Vue({
    el: '#app',
    data: {
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
        list_laughtpictures:[
            {image:'../../static/res/laughtpicture/6a0f5341-42ac-4dcf-83cd-f92f6fa8876c.gif'},
            {image:'../../static/res/laughtpicture/6045d699-54c7-4653-a5c3-3ea94889d69f.gif'},
            {image:'../../static/res/laughtpicture/52869ff5-8110-45fa-8267-d2c93e2fef0f.gif'},
            {image:'../../static/res/laughtpicture/9592291d-9f88-4c42-adc4-31736c72f96c.gif'},
            {image:'../../static/res/laughtpicture/20788815-9488-4e75-8368-7ce34274a025.gif'},
            {image:'../../static/res/laughtpicture/u=1473546188,1786515403&fm=173&s=B2165384080706D8462479810300F0CA&w=605&h=706&img.jpeg'},
            {image:'../../static/res/laughtpicture/u=3071455273,120725408&fm=27&gp=0.jpg'},
        ],
        },
        methods: {
        handleSortChange ({name, order}) {
            this.list = this.list.sort((a, b) => order === 'asc' ? a[name] - b[name] : b[name] - a[name]);
          }
    },
    watch: {
    },
});