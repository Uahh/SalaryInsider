v = {
    name: "Form",
    data() {
        return {
            chooseShow: true,
            createShow: false,
            joinShow: false,
            waitShow: false,
            copyShow: false,
            resultShow: false,
            times: null,
            form: {
                salary: '',
                salaryType: '月薪',
                roomNumber: '',
                roomPeople: '',
                nowPeople: 1
            },
        };
    },
    methods: {
        onCreate() {
            this.createShow = true;
            this.chooseShow = false;
        },
        onJoin() {
            this.joinShow = true;
            this.chooseShow = false;
        },
        onBack() {
            this.joinShow = false;
            this.createShow = false;
            this.chooseShow = true;
        },
        onSubmitCreate() {
            if (this.isNumber(this.form.salary) && this.isNumber(this.form.roomPeople)) {
                if (this.form.roomPeople < 2) {
                    this.$message({
                        message: '人数不能少于1',
                        type: 'error'
                    });
                    return
                }
                this.joinShow = false;
                this.createShow = false;
                this.waitShow = true;
                this.copyShow = true;
                let res = axios({
                    method: 'post',
                    url: '/create_room',
                    data: this.form,
                })
                    .then((res) => {
                        this.form.roomNumber = res['data']
                        this.createInterval()
                    })
                    .catch((error) => {
                    }).finally(() => {
                    });
            }
            else {
                this.$message({
                    message: '创建失败，请检查填写信息',
                    type: 'error'
                });
            }
        },
        onSubmitJoin() {
            if (this.form.roomNumber != '' && this.isNumber(this.form.salary)) {
                this.res = axios({
                    method: 'post',
                    url: '/join_room',
                    data: this.form,
                })
                    .then((res) => {
                        console.log(typeof (res['data']))
                        if (typeof (res['data']) != 'string') {
                            this.form.nowPeople = res['data']['nowPeople']
                            this.form.roomPeople = res['data']['roomPeople']
                            if (res['data']['resultSalary'] != -1) {
                                this.waitShow = false;
                                this.resultShow = true;
                                this.form.salary = res['data']['resultSalary']
                            }
                            else {
                                this.createInterval()
                            }
                            this.joinShow = false;
                            this.chooseShow = false;
                            this.waitShow = true;
                            this.copyShow = false;
                        }
                        else {
                            this.$message({
                                message: res['data'],
                                type: 'error'
                            });
                        }
                    })
                    .catch((error) => {
                    }).finally(() => {
                    });
            }
            else {
                this.$message({
                    message: '加入失败，请检查填写信息',
                    type: 'error'
                });
            }
        },
        onCopy() {
            var val = document.getElementById('needCopy');
            window.getSelection().selectAllChildren(val);
            document.execCommand("Copy");
            this.$message({
                message: '复制成功',
                type: 'success'
            });
        },
        createInterval() {
            this.times = setInterval(() => {
                this.getPeople();
            }, 1000 * 3);
        },
        getPeople() {
            let res = axios({
                method: 'post',
                url: '/get_people',
                data: {
                    id: this.form.roomNumber,
                    nowPeople: this.form.nowPeople
                }
            })
                .then((res) => {
                    this.form.nowPeople = res['data']['nowPeople']
                    console.log(res)
                    if (res['data']['resultSalary'] != -1) {
                        this.waitShow = false;
                        this.resultShow = true;
                        this.form.salary = res['data']['resultSalary']
                        clearInterval(this.times);
                    }
                })
        },
        // 判断是否是数字
        isNumber(value) {
            return (typeof value === 'number' && !isNaN(value));
        }
    }
}
const V = Vue.createApp(v);
V.use(ElementPlus);
V.mount("#app");