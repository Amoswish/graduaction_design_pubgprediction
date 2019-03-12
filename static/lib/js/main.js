new Vue({
    // delimiters: ['{[', ']}'],
    el: '#app',
    component: {
    },
    data: {
      screenwidth:100,
      screenheight:100,
      leaderboard_data:[
        ["1", "Murad_Gazdiev", "7,415", "4818", "1.6%", "13.0%", "1.41", "173", "#45.4"],
        ["1", "Murad_Gazdiev", "7,415", "4818", "1.6%", "13.0%", "1.41", "173", "#45.4"],
        ["1", "Murad_Gazdiev", "7,415", "4818", "1.6%", "13.0%", "1.41", "173", "#45.4"],
        ["1", "Murad_Gazdiev", "7,415", "4818", "1.6%", "13.0%", "1.41", "173", "#45.4"],
        ["1", "Murad_Gazdiev", "7,415", "4818", "1.6%", "13.0%", "1.41", "173", "#45.4"],
      ],
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
        leaderboard_columns: [
              { title: '排名', width: 200, name: 'name' },
              { title: '用户🆔', name: 'playerid', width: 126, align: 'center', sortable: true },
              { title: 'SP', name: 'plyaersp', width: 126, align: 'center', sortable: true },
              { title: '游戏场数', name: 'playergametimes', width: 126, align: 'center', sortable: true },
              { title: '胜%', name: 'winpercent', width: 126, align: 'center', sortable: true },
              { title: 'Top 10%', name: 'playertop10percent', width: 126, align: 'center', sortable: true },
              { title: 'K/D', name: 'playerkd', width: 126, align: 'center', sortable: true },
              { title: '伤害', name: 'playerdamage', width: 126, align: 'center', sortable: true },
              { title: '平均排名', name: 'playeravgrank', width: 126, align: 'center', sortable: true },
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
          console.log(this.screenheight);
        },
        submit(){
            var that = this;
            // 对应 Python 提供的接口，这里的地址填写下面服务器运行的地址，本地则为127.0.0.1，外网则为 your_ip_address
            const path = 'http://127.0.0.1:5000/getMsg';
            axios.get(path).then(function (response) {
                // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串
                // 可以直接通过 response.data 取key-value
                // 坑一：这里不能直接使用 this 指针，不然找不到对象
                var msg = response.data.msg;
                // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串
                that.serverResponse = msg;

                alert('Success ' + response.status + ', ' + response.data + ', ' + msg);
                }).catch(function (error) {
                alert('Error ' + error);
            })
        }
    },
    watch:{
      shift:function(newshift,oldshift){
        if(newshift=='leaderboard'){
          axios.get('/leaderboardjson')
            .then(function (response) {
              console.log(response);
            })
            .catch(function (error) {
              console.log(error);
            });
        }
      },
    },
});