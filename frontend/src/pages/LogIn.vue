<template>
  <v-main box>
    <!-- <v-container> -->
    <div class="cont">
      <div class="cont_center_left">
        <div v-if="nm_page === 0" class="start">
          <div>
            <h1>일반회원</h1>
            <v-btn rounded color="rgb(0,0,0)" dark @click="mvpage(true)"
              >시작하기</v-btn
            >
          </div>
        </div>
        <div v-if="nm_page === 1" class="start">
          <div class="inputform">
            <div>
              <button @click="reset(true)">
                <i class="material-icons">&#xE5C4;</i>
              </button>
              <h1>일반회원</h1>
            </div>
            <v-text-field v-model="nm_email" label="이메일"></v-text-field>
            <v-text-field
              v-model="nm_password"
              label="비밀번호"
              :append-icon="showpassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showpassword ? 'text' : 'password'"
              @click:append="showpassword = !showpassword"
            ></v-text-field>
            <v-btn rounded color="rgb(233, 105, 30)" dark @click="checkLogin()"
              >로그인</v-btn
            >
            <v-btn rounded color="rgb(0,0,0)" dark @click="mvpage(true)"
              >회원등록</v-btn
            >
          </div>
        </div>
        <div v-if="nm_page === 2" class="start">
          <div class="inputform">
            <div>
              <button @click="reset(true)">
                <i class="material-icons">&#xE5C4;</i>
              </button>
              <h1>일반회원</h1>
            </div>
            <v-text-field
              v-model="nm_email"
              :messages="[error.email]"
              label="이메일"
              ref="nm_email"
            ></v-text-field>
            <v-text-field v-model="nm_name" label="이름"></v-text-field>
            <v-text-field v-model="nm_nickname" label="닉네임"></v-text-field>
            <v-text-field
              v-model="nm_password"
              :messages="[error.pwd]"
              label="비밀번호"
              ref="nm_password"
              :append-icon="showpassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showpassword ? 'text' : 'password'"
              @click:append="showpassword = !showpassword"
            ></v-text-field>
            <v-text-field
              v-model="nm_password_confirm"
              :messages="[error.pwdconfirm]"
              label="비밀번호 확인"
              ref="nm_password_confirm"
              :append-icon="showpasswordConfirm ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showpasswordConfirm ? 'text' : 'password'"
              @click:append="showpasswordConfirm = !showpasswordConfirm"
            ></v-text-field>
            <v-text-field
              label="주소"
              @click="findAddress(true)"
              readonly="readonly"
              v-model="nm_address"
            ></v-text-field>
            <v-container fluid style="height:fit-content;">
              <v-layout style="height:fit-content;" row>
                <v-radio-group v-model="nm_gender" row>
                  <v-flex xs4>
                    <label for="nm_gender">성별</label>
                  </v-flex>
                  <v-flex xs4>
                    <v-radio label="FEMALE" value="1"></v-radio>
                  </v-flex>
                  <v-flex xs4>
                    <v-radio label="MALE" value="0"></v-radio>
                  </v-flex>
                </v-radio-group>
              </v-layout>
            </v-container>
            <v-text-field
              label="출생년도"
              type="number"
              v-model="nm_birthyear"
            ></v-text-field>
            <v-btn rounded color="rgb(0,0,0)" dark @click="checkHandler()"
              >회원가입</v-btn
            >
          </div>
        </div>
      </div>
      <div class="cont_center_right">
        <div v-if="biz_page === 0" class="start">
          <div>
            <h1>사업자회원</h1>
            <v-btn rounded color="rgb(0,0,0)" dark @click="mvpage(false)"
              >시작하기</v-btn
            >
          </div>
        </div>
        <div v-if="biz_page === 1" class="start">
          <div class="inputform">
            <div>
              <button @click="reset(false)">
                <i class="material-icons">&#xE5C4;</i>
              </button>
              <h1>사업자회원</h1>
            </div>
            <v-text-field
              v-model="biz_email"
              ref="biz_email"
              label="사업자이메일"
            ></v-text-field>
            <v-text-field
              v-model="biz_password"
              ref="biz_password"
              label="비밀번호"
              :append-icon="showbizpassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showbizpassword ? 'text' : 'password'"
              @click:append="showbizpassword = !showbizpassword"
            ></v-text-field>
            <v-btn
              rounded
              color="rgb(233, 105, 30)"
              dark
              @click="checkBizLogin()"
              >로그인</v-btn
            >
            <v-btn rounded color="rgb(0,0,0)" dark @click="mvpage(false)"
              >사업자등록</v-btn
            >
          </div>
        </div>
        <div v-if="biz_page === 2" class="start">
          <div class="inputform">
            <div>
              <button @click="reset(false)">
                <i class="material-icons">&#xE5C4;</i>
              </button>
              <h1>사업자회원</h1>
            </div>
            <v-text-field
              v-model="biz_email"
              :messages="[error.bizemail]"
              ref="biz_email"
              label="사업자이메일"
            ></v-text-field>
            <v-text-field
              v-model="biz_numb"
              ref="biz_numb"
              label="사업자번호"
            ></v-text-field>
            <v-file-input
              accept="image/*"
              label="사업자등록사본"
              v-model="biz_image"
            ></v-file-input>
            <!-- <picture-input
              @change="onChanged"
              @remove="onRemoved"
              :width="500"
              :removable="true"
              removeButtonClass="ui red button"
              :height="500"
              accept="image/jpeg, image/png, image/gif, image/jpg"
              buttonClass="ui button primary"
              :customStrings="{
              upload: '<h1>Upload it!</h1>',
              drag: 'Drag and drop your image here'}">
            </picture-input>   -->
            <v-text-field
              v-model="biz_name"
              ref="biz_name"
              label="업주명"
            ></v-text-field>
            <v-text-field
              v-model="biz_password"
              ref="biz_password"
              :messages="[error.bizpwd]"
              label="비밀번호"
              :append-icon="showbizpassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showbizpassword ? 'text' : 'password'"
              @click:append="showbizpassword = !showbizpassword"
            ></v-text-field>
            <v-text-field
              v-model="biz_password_confirm"
              ref="biz_password_confirm"
              :messages="[error.bizpwdconfirm]"
              label="비밀번호 확인"
              :append-icon="showbizpasswordConfirm ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showbizpasswordConfirm ? 'text' : 'password'"
              @click:append="showbizpasswordConfirm = !showbizpasswordConfirm"
            ></v-text-field>
            <v-text-field
              v-model="biz_address"
              label="사업장주소"
              readonly="readonly"
              @click="findAddress(false)"
            ></v-text-field>
            <v-btn rounded color="rgb(0,0,0)" dark @click="checkBizHandler()"
              >회원가입</v-btn
            >
          </div>
        </div>
      </div>
    </div>
    <!-- </v-container> -->
  </v-main>
</template>

<script src="http://dmaps.daum.net/map_js_init/postcode.v2.js"></script>
<script src="//dapi.kakao.com/v2/maps/sdk.js?appkey=48cbffa8392e1a7acffc1975347ec0d3&libraries=services"></script>

<script>
import axios from "axios";
import * as firebase from "firebase";
import { mapMutations, mapGetters, mapState } from "vuex";

// const baseURL = "http://127.0.0.1:8000/";
const baseURL = "http://ec2-52-79-239-80.ap-northeast-2.compute.amazonaws.com/";
export default {
  name: "LogIn",
  data() {
    return {
      showpassword: false,
      showpasswordConfirm: false,
      nm_page: 0,
      nm_email: "",
      nm_name: "",
      nm_nickname: "",
      nm_password: "",
      nm_password_confirm: "",
      nm_address: "",
      nm_gender: "",
      nm_birthyear: 1990,
      nm_check: false,

      showbizpassword: false,
      showbizpasswordConfirm: false,
      biz_page: 0,
      biz_numb: "",
      biz_email: "",
      biz_name: "",
      biz_password: "",
      biz_password_confirm: "",
      biz_address: "",
      biz_image: "",

      error: {
        email: "",
        pwd: "",
        pwdconfirm: "",
        biznumb: "",
        bizemail: "",
        bizpwd: "",
        bizpwdconfirm: "",
      },
      password: "password",

      rules: [
        {
          message: "이메일을 확인해주세요",
          regex: /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/,
        },
        {
          message: "사용불가능한 비밀번호입니다",
          regex: /(?=.*\d)(?=.*[a-z]).{8,}/,
        },
      ],
    };
  },
  watch: {
    nm_email: function() {
      var domain = ["@naver.com", "@daum.net", "@hanmail.net", "@gmail.com"];
      if (this.nm_email.length > 0) {
        for (var i = 0; i < domain.length; i++) {
          if (this.nm_email.includes(domain[i])) {
            this.nm_check = true;
            break;
          }
          this.nm_check = false;
        }
        if (!this.nm_check) {
          this.error.email = this.rules[0].message;
          return;
        }
        this.error.email = "";
        this.nm_nickname = this.nm_email;
        axios
          .post(baseURL + "api/accounts/user_email/", {
            email: this.nm_email,
          })
          .then((res) => {
            if (res.data.message === "이미 존재하는 이메일입니다.") {
              this.error.email = "이미 존재하는 이메일입니다.";
            }
          });
      }
    },
    biz_numb: function() {
      if (this.biz_numb.length > 0) {
        if (this.biz_numb.length > 12) {
          this.bizlen();
          return;
        }
        if (this.biz_numb.length == 3 || this.biz_numb.length == 6)
          this.biz_numb += "-";
        if (!this.checkBizNumb()) {
          this.error.biznumb = "존재하지 않는 사업자번호입니다.";
          return;
        }
        this.error.biznumb = "";
      }
    },
    biz_email: function() {
      var domain = ["@naver.com", "@daum.net", "@hanmail.net", "@gmail.com"];
      if (this.biz_email.length > 0) {
        for (var i = 0; i < domain.length; i++) {
          if (this.biz_email.includes(domain[i])) {
            this.biz_check = true;
            break;
          }
          this.biz_check = false;
        }
        if (!this.biz_check) {
          this.error.bizemail = this.rules[0].message;
          return;
        }
        this.error.bizemail = "";
        axios
          .post(baseURL + "api/accounts/user_email/", {
            email: this.biz_email,
          })
          .then((res) => {
            if (res.data.message === "이미 존재하는 이메일입니다.") {
              this.error.bizemail = "이미 존재하는 이메일입니다.";
            }
          });
      }
    },
    nm_password: function() {
      var temp = ["qwert", "asdfg", "zxcvb", "1234"];
      var nm_password = this.nm_password;
      if (this.nm_password.length > 0) {
        for (var t in temp) {
          if (this.nm_password.includes(temp[t])) {
            this.error.pwd = this.rules[1].message;
            return;
          }
        }
        this.error.pwd = this.rules[1].message;
        if (!this.rules[1].regex.test(nm_password)) {
          this.error.pwd = this.rules[1].message;
          return;
        }
        this.error.pwd = "";
        return;
      }
    },
    biz_password: function() {
      var temp = ["qwert", "asdfg", "zxcvb"];
      if (this.biz_password.length > 0) {
        for (var t in temp) {
          if (this.biz_password.includes(temp[t])) {
            this.error.bizpwd = this.rules[1].message;
            return;
          }
        }
        if (!this.rules[1].regex.test(this.biz_password)) {
          this.error.bizpwd = this.rules[1].message;
          return;
        }
        this.error.bizpwd = "";
        return;
      }
    },
    nm_password_confirm: function() {
      if (this.nm_password_confirm.length > 0) {
        if (this.nm_password_confirm !== this.nm_password) {
          this.error.pwdconfirm = "비밀번호가 틀렸습니다";
          return;
        }
        this.error.pwdconfirm = "";
      }
    },
    biz_password_confirm: function() {
      if (this.biz_password_confirm.length > 0) {
        if (this.biz_password_confirm !== this.biz_password) {
          this.error.bizpwdconfirm = "비밀번호가 틀렸습니다";
          return;
        }
        this.error.bizpwdconfirm = "";
      }
    },
  },

  computed: {
    // comparePasswords () {
    //     return this.password !== this.confirmPassword ? 'Passwords do not match.' : true
    //   },
    ...mapGetters("server", ["getBaseURL"]),
    ...mapGetters("userInfo", ["getIsLogin"]),
    ...mapState("server", ["baseURL"]),
  },

  created() {
    console.log(this.getBaseURL); // 예상은 아마존 서버가 찍혀야되는데
  },

  methods: {
    ...mapMutations(("userInfo", ["setUserInfo"])),
    ...mapMutations(("userInfo", ["setIsLogin"])),
    ...mapMutations(("userInfo", ["setUserType"])),
    bizlen() {
      var temp = this.biz_numb.substring(0, 12);
      this.biz_numb = temp;
      return this.biz_numb;
    },
    checkHandler() {
      let err = true;
      let msg = "";
      !this.nm_email &&
        ((msg = "이메일을 입력해주세요!"),
        (err = false),
        this.$refs.nm_email.focus());
      err &&
        !this.nm_password &&
        ((msg = "비밀번호를 입력해주세요!"),
        (err = false),
        this.$refs.nm_password.focus());
      err &&
        !this.nm_password_confirm &&
        ((msg = "비밀번호 확인을 입력해주세요!"),
        (err = false),
        this.$refs.nm_password_confirm.focus());
      if (!err) {
        alert(msg);
      } else if (
        !this.error.email &&
        !this.error.password &&
        !this.error.passwordConfirm
      ) {
        this.nm_signup();
      }
    },
    checkBizHandler() {
      let err = true;
      let msg = "";
      !this.biz_email &&
        ((msg = "이메일을 입력해주세요!"),
        (err = false),
        this.$refs.biz_email.focus());
      err &&
        !this.biz_numb &&
        ((msg = "사업자번호를 입력해주세요!"),
        (err = false),
        this.$refs.biz_numb.focus());
      err &&
        !this.biz_name &&
        ((msg = "이름을 입력해주세요!"),
        (err = false),
        this.$refs.biz_name.focus());
      err &&
        !this.biz_password &&
        ((msg = "비밀번호를 입력해주세요!"),
        (err = false),
        this.$refs.biz_password.focus());
      err &&
        !this.biz_password_confirm &&
        ((msg = "비밀번호 확인을 입력해주세요!"),
        (err = false),
        this.$refs.biz_password_confirm.focus());
      if (!err) {
        alert(msg);
      } else if (!this.checkBizNumb()) {
        alert("사업자번호가 올바르지 않습니다.");
      } else if (!this.checkBizNumb()) {
        alert("사업자번호가 올바르지 않습니다.");
      }
      if (err) {
        this.biz_signup();
      }
    },
    checkLogin() {
      let err = true;
      let msg = "";
      !this.nm_email &&
        ((msg = "이메일을 입력해주세요!"),
        (err = false),
        this.$refs.nm_email.focus());
      err &&
        !this.nm_password &&
        ((msg = "비밀번호를 입력해주세요!"),
        (err = false),
        this.$refs.nm_password.focus());
      if (err) {
        this.nm_login();
      }
    },

    findAddress(check) {
      new daum.Postcode({
        oncomplete: (data) => {
          var fullAddr = data.address;
          var extraAddr = "";

          if (data.addressType === "R") {
            if (data.bname !== "") {
              extraAddr += data.bname;
            }
            if (data.buildingName !== "") {
              extraAddr +=
                extraAddr !== "" ? ", " + data.buildingName : data.buildingName;
            }
            fullAddr += extraAddr !== "" ? " (" + extraAddr + ")" : "";
            if (check) this.nm_address = fullAddr;
            else this.biz_address = fullAddr;
          } else {
            if (check) this.nm_address = fullAddr;
            else this.biz_address = fullAddr;
          }
        },
      }).open();
    },

    setCookie(token) {
      this.$cookies.set("auth-token", token);
    },
    setCookie(token, nickname) {
      this.$cookies.set("auth-token", token);
      this.$cookies.set("nickname", nickname);
    },

    onSignin() {
      this.$store.dispatch("signUserIn", {
        email: this.nm_email,
        password: this.nm_password,
      });
    },

    nm_login() {
      var tmpToken;
      axios
        .post(baseURL + "api/accounts/email_user_or_bizuser/", {
          email: this.nm_email,
        })
        .then((res) => {
          if (res.data.message == 1) {
            axios
              .post(baseURL + "api/account/login/", {
                email: this.nm_email,
                password: this.nm_password,
              })
              .then((res) => {
                this.setCookie(res.data.key);
                tmpToken = res.data.key;
                axios
                  .post(baseURL + "api/accounts/user_nickname/", null, {
                    headers: {
                      Authorization: `Token ${res.data.key}`,
                    },
                  })
                  .then((res) => {
                    this.$cookies.set("nickname", res.data.nickname);
                    axios
                      .post(baseURL + "api/accounts/profile/", null, {
                        headers: {
                          Authorization: `Token ${tmpToken}`,
                        },
                      })
                      .then((res) => {
                        this.$store.commit("userInfo/setUserInfo", {
                          userAddress: res.data.address,
                        });
                        localStorage.setItem("isLogin", true);

                        this.$router.push("/home");
                      })
                      .catch((err) => {
                        console.log("get profile error", err);
                      });
                  })
                  .catch((err) => {
                    console.log("get nickname error", err.response);
                  });
              })
              .catch((err) => {
                console.log(err);
                alert("로그인 정보를 다시 확인하시지요");
              });
          } else {
            alert("존재하지 않는 회원 정보입니다.");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    checkBizLogin() {
      let err = true;
      let msg = "";
      !this.biz_email &&
        ((msg = "이메일을 입력해주세요!"),
        (err = false),
        this.$refs.biz_email.focus());
      err &&
        !this.biz_password &&
        ((msg = "비밀번호를 입력해주세요!"),
        (err = false),
        this.$refs.biz_password.focus());
      if (err) this.biz_login();
    },
    biz_login() {
      axios
        .post(baseURL + "api/accounts/email_user_or_bizuser/", {
          email: this.biz_email,
        })
        .then((res) => {
          if (res.data.message == 0) {
            axios
              .post(baseURL + "api/account/login/", {
                email: this.biz_email,
                password: this.biz_password,
              })
              .then((res) => {
                axios
                  .post(baseURL + "api/accounts/profile/", null, {
                    headers: {
                      Authorization: `Token ${tmpToken}`,
                    },
                  })
                  .then((res) => {
                    this.$store.commit("userInfo/setUserType", {
                      userAddress: res.data.usertype,
                    });

                    localStorage.setItem("isLogin", true);
                    this.setCookie(res.data.key);
                    this.$router.push("/home");
                  })
                  .catch((err) => {
                    console.log("get profile error", err);
                  });
                // })
              })
              .catch((err) => {
                alert("아이디 또는 비밀번호를 확인해주세요.");
              });
          } else {
            alert("존재하지 않는 회원 정보입니다.");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },

    checkBizNumb() {
      var valueMap = this.biz_numb
        .replace(/-/gi, "")
        .split("")
        .map(function(item) {
          return parseInt(item, 10);
        });

      if (valueMap.length === 10) {
        var multiply = new Array(1, 3, 7, 1, 3, 7, 1, 3, 5);
        var checkSum = 0;

        for (var i = 0; i < multiply.length; ++i) {
          checkSum += multiply[i] * valueMap[i];
        }

        checkSum += parseInt((multiply[8] * valueMap[8]) / 10, 10);
        return Math.floor(valueMap[9]) === 10 - (checkSum % 10);
      }

      return false;
    },

    nm_signup() {
      var tmpToken = "";

      axios
        .post(baseURL + "api/account/signup/", {
          username: this.nm_nickname,
          email: this.nm_email,
          password1: this.nm_password,
          password2: this.nm_password_confirm,
        })
        .then((res) => {
          // post > then
          tmpToken = res.data.key;

          axios
            .post(
              // post > post
              baseURL + "api/accounts/user_detail/",
              {
                username: this.nm_nickname,
                email: this.nm_email,
                usertype: 1,
                gender: this.nm_gender,
                address: this.nm_address,
                birth_year: this.nm_birthyear,
              },
              {
                headers: {
                  Authorization: `Token ${res.data.key}`,
                },
              }
            )
            .then((res) => {
              // post > post > then
              axios
                .post(
                  // post > post > post
                  baseURL + "api/accounts/user_order/",
                  {
                    location: this.nm_address,
                  },
                  {
                    headers: {
                      Authorization: "Token " + tmpToken,
                    },
                  }
                ) // post > post > post > thrn
                .then((res) => {
                  console.log(res.data);
                  this.reset(true);
                  this.$router.push("/");
                })
                .catch((res) => {
                  console.log("user_order error", res);
                }); // post > post > post > catch
            })
            .catch((res) => {
              console.log("user_detail error", res);
            }); // post > post > catch
        })
        .catch((err) => {
          console.log("signup error", err);
        }); // post > catch
    },
    biz_signup() {
      axios
        .post(baseURL + "api/account/signup/", {
          username: this.biz_name,
          email: this.biz_email,
          password1: this.biz_password,
          password2: this.biz_password_confirm,
        })
        .then((res) => {
          const formData = new FormData();
          formData.append("email", this.biz_email);
          formData.append("username", this.biz_name);
          formData.append("usertype", 0);
          formData.append("bizname", this.biz_name);
          formData.append("bizaddress", this.biz_address);
          formData.append("bizimage", this.biz_image);
          axios
            .post(baseURL + "api/accounts/user_detail/", formData, {
              headers: {
                Authorization: `Token ${res.data.key}`,
              },
            }) // post > post
            .then((res) => {
              this.reset(false);
              this.$router.push("/");
            })
            .catch((err) => {
              // err.response
              // let token = res.data.key;
              console.log("error : " + err);
              console.log(err.response);
              // this.$store.dispatch("signUserUp", {
              //   email: this.nm_email,
              //   password: this.nm_password,
              //   username: this.nm_nickname,
              // });
            });
        })
        .catch((err) => {
          console.log(err);
        });
    },
    reset(nm) {
      if (nm) {
        this.nm_page -= 1;
        this.nm_email = "";
        this.nm_name = "";
        this.nm_nickname = "";
        this.nm_password = "";
        this.nm_password_confirm = "";
        this.nm_address = "";
        this.nm_gender = "";
        this.nm_birthyear = "1990";
        this.showpassword = false;
        this.showpasswordConfirm = false;
      } else {
        this.biz_page -= 1;
        this.biz_email = "";
        this.biz_name = "";
        this.biz_password = "";
        this.biz_password_confirm = "";
        this.biz_address = "";
        this.showbizpassword = false;
        this.showbizpasswordConfirm = false;
      }
      this.error = {
        email: "",
        pwd: "",
        pwdconfirm: "",
        bizemail: "",
        bizpwd: "",
        bizpwdconfirm: "",
      };
    },
    mvpage(nm) {
      if (nm) {
        this.biz_page = 0;
        this.nm_page += 1;
        this.nm_email = "";
        this.nm_name = "";
        this.nm_nickname = "";
        this.nm_password = "";
        this.nm_password_confirm = "";
        this.nm_address = "";
        this.nm_gender = "";
        this.nm_birthyear = "1990";
        this.showpassword = false;
        this.showpasswordConfirm = false;
      } else {
        this.nm_page = 0;
        this.biz_page += 1;
        this.biz_email = "";
        this.biz_name = "";
        this.biz_password = "";
        this.biz_password_confirm = "";
        this.biz_address = "";
        this.showbizpassword = false;
        this.showbizpasswordConfirm = false;
      }
      this.error = {
        email: "",
        pwd: "",
        pwdconfirm: "",
        bizemail: "",
        bizpwd: "",
        bizpwdconfirm: "",
      };
    },
  },
};
</script>
<style scoped src="../assets/css/login.css">
.cont {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}
.cont::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera*/
}
</style>
