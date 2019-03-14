new Vue({
    // delimiters: ['{[', ']}'],
    el: '#app',
    component: {
    },
    data: {
      screenwidth:100,
      screenheight:100,
      leaderboard_mode:'fpp',
      opensubmitresult: false,
      openadvicediog:false,
      predictresult:'',
      advice:'',
      leaderboard_teamsize:1,
      leaderboard_data:[],
      input_data_form:{
        assists: 30,
        boosts: 30,
        damageDealt: 30,
        DBNOs: 30,
        headshotKills: 30,
        heals: 30,
        killPlace: 30,
        killPoints: 30,
        kills: 30,
        killStreaks: 30,
        longestKill: 30,
        matchDuration: 30,
        matchType_select:'',
        maxPlace: 30,
        numGroups: 30,
        rankPoints: 30,
        revives: 30,
        rideDistance: 30,
        roadKills: 30,
        swimDistance: 30,
        teamKills: 30,
        vehicleDestroys: 30,
        walkDistance: 30,
        weaponsAcquired: 30,
        winPoints: 30,
      },
      matchType_type: [
        '单排', '双排', '四排'
        ],
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
        chart_map: 'erangel',
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
    },
    methods: {
        handleSortChange ({name, order}) {
            this.leaderboard_data = this.leaderboard_data.sort((a, b) => order === 'asc' ? a[name] - b[name] : b[name] - a[name]);
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
        changemode(mode){
          console.log('sss', '')
          this.leaderboard_mode = mode
          let _this = this
          const path = '/leaderboardjson'
          let params = new URLSearchParams();
          params.append('mode',_this.leaderboard_mode)
          params.append('teamsize',_this.leaderboard_teamsize)
          console.log(params)
          axios.post(path,params)
          .then(function (response) {
            console.log(response.data);
            _this.leaderboard_data = response.data
          })
          .catch(function (error) {
            console.log(error);
          });
        },
        changeteamsize(teamsize){
          this.leaderboard_teamsize = teamsize
          let _this = this
          const path = '/leaderboardjson'
          let params = new URLSearchParams();
          params.append('mode',_this.leaderboard_mode)
          params.append('teamsize',_this.leaderboard_teamsize)
          console.log(params)
          axios.post(path,params)
          .then(function (response) {
            console.log(response.data);
            _this.leaderboard_data = response.data
          })
          .catch(function (error) {
            console.log(error);
          });
        },
        submit(){
            this.opensubmitresult = true;
            let _this = this;
            // 对应 Python 提供的接口，这里的地址填写下面服务器运行的地址，本地则为127.0.0.1，外网则为 your_ip_address
            const path = '/getWinprec';
            let params = new URLSearchParams();
            //将obj转化为array
            for(let key in _this.input_data_form){
                params.append(key,_this.input_data_form[key])
            }

            axios.post(path,params)
            .then(function (response) {
                // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串
                // 可以直接通过 response.data 取key-value
                // 坑一：这里不能直接使用 this 指针，不然找不到对象
                var msg = response.data.msg;
                // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串
                _this.serverResponse = msg;
                _this.predictresult = msg;
            })
        },
        closesubmitDialog () {
          this.opensubmitresult = false;
        },
        openAdviceDialog () {
          this.opensubmitresult = false;
          this.openadvicediog = true;
          let _this = this;
          // 对应 Python 提供的接口，这里的地址填写下面服务器运行的地址，本地则为127.0.0.1，外网则为 your_ip_address
          const path = '/getAdvice';
          let params = new URLSearchParams();
          //将obj转化为array
          for(let key in _this.input_data_form){
              params.append(key,_this.input_data_form[key])
          }

          axios.post(path,params)
          .then(function (response) {
              // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串
              // 可以直接通过 response.data 取key-value
              // 坑一：这里不能直接使用 this 指针，不然找不到对象
              var msg = response.data.msg;
              // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串
              _this.serverResponse = msg;
              _this.advice = msg;
          })
        },
        closeAdviceDialog () {
          this.openadvicediog = false;
          this.advice = ''
        }
    },
    watch:{
      shift:function(newshift,oldshift){
        if(newshift=='leaderboard'){
            let _this = this
            const path = '/leaderboardjson'
            let params = new URLSearchParams();
            params.append('mode',_this.leaderboard_mode)
            params.append('teamsize',_this.leaderboard_teamsize)
            console.log(params)
            axios.post(path,params)
            .then(function (response) {
              console.log(response.data);
              _this.leaderboard_data = response.data
            })
            .catch(function (error) {
              console.log(error);
            });
        }
      },
    },
});