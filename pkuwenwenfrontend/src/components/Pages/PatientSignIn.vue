<template>
<div>
    <div id="navbar">
      <router-link to="/">Home</router-link> |
      <router-link to="/DoctorSignIn">Doctor Sign In</router-link> |
      <router-link to="/PatientSignIn">Patient Sign In</router-link> |
      <router-link to="/SignUpAsPatient">Sign Up as Patient</router-link> |
      <router-link to="/SignUpAsDoctor">Sign Up as Doctor</router-link>
    </div>
    <div>
        <img alt="Vue logo" src="../../assets/logo2.jpeg">
    </div>
    <div class="ms-login">
      <div class="ms-title">北大医院登陆</div>
      <el-form :model="param" :rules="rules" ref="login" label-width="0px" class="ms-content">
        <el-form-item prop="username">
          <el-input v-model="param.username" placeholder="请输入用户名">
            <template #prepend>
              <el-button icon="el-icon-user"></el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
              type="password"
              placeholder="请输入密码"
              v-model="param.password"
              @keyup.enter="submitForm()"
          >
            <template #prepend>
              <el-button icon="el-icon-lock"></el-button>
            </template>
          </el-input>
        </el-form-item>
        <div class="login-btn">
          <el-button type="primary" @click="submitForm()">登录</el-button>
        </div>
      </el-form>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            param: {
                username: '',
                password: '',
            },
            rules: {
                username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
                password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
            },
        };
    },
    methods: {
        submitForm() {
            var post_request = new FormData()
            post_request.append('userName', this.param.username)
            post_request.append('password', this.param.password)
            post_request.append('type', 'patient')
            //let _this = this;
            this.$http
            .request({
              url: this.$url + '/login',
              method: 'post',
              data: post_request,
              headers: { 'Content-Type': 'multipart/form-data' },
            })
            .then((response) =>{
              console.log(response)
              // if(response.data.login.retCode == 1){  //这行在最后需要代替下面的 if true
              // eslint-disable-next-line no-constant-condition
              if(response.data.login.retCode == 1){
                alert('登陆成功');
                /*
                this.$message({
                    showClose: true,
                    message:'登录成功'
                })
                */
                localStorage.setItem("ms_username", this.param.username)
                this.$router.push('/PatientHomepage');
              }
              else if(response.data.login.retCode == 2) {
                /*_this.$message({
                    message: response.data.login.message,
                    type: 'error',
                });
                */
               alert('密码错误！');
                return false
              }
              else {
                /*
                _this.$message({
                    message: response.data.login.message + "！请先注册",
                    type: 'warning',
                });*/
                alert('用户不存在，请先注册！');
                return false
              }

            })
            .catch((response) => {
              console.log(response)
            });
        },
    },
};
</script>

<style scoped>
.head {
    width: 100%;
    height: 70px;
    background-color: #324157;
}
.head button {
    float: right;
    height: 36px;
    margin-left: 10px;
    margin-top: 15px;
}
.ms-title {
    width: 100%;
    line-height: 50px;
    text-align: center;
    font-size: 40px;
    color: #F56C6C;
    border-bottom: 1px solid #ddd;
}
.ms-login {
    position: absolute;
    left: 50%;
    top: 20%;
    width: 350px;
    margin: 190px 0 0 -175px;
    border-radius: 5px;
    background: rgba(255, 255, 255, 0.3);
    overflow: hidden;
}
.ms-content {
    padding: 30px 30px;
}
.login-btn {
    text-align: center;
}
.login-btn button {
    width: 100%;
    height: 36px;
    margin-bottom: 10px;
}
.login-tips {
    font-size: 12px;
    line-height: 30px;
    color: #fff;
}


</style>
