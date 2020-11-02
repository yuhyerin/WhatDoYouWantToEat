<template>
  <v-container fluid>
    <div
      class="review-write"
      style="border: 1px solid silver; margin-bottom: 30px; border-radius: 0.4em"
    >
      <div style="margin:10px" v-show="loginUsertype == 1">
        <v-rating
          v-model="rating"
          style="text-align:left"
          background-color="orange lighten-3"
          color="orange"
          dense="true"
          half-increments="true"
          hover="true"
        ></v-rating
        ><br />
        <v-textarea
          outlined
          name="input-7-4"
          label="리뷰를 남겨보세요."
          v-model="myReview"
          color="rgb(233, 105, 30)"
        ></v-textarea>
        <div class="text-right">
          <v-btn
            v-show="rating == 0 || myReview == 0"
            @click="msg()"
            color="gray"
            style="color:darkgray; margin-top: -15px"
            >등록</v-btn
          >
          <v-btn
            v-show="rating > 0 && myReview != 0"
            @click="registerReview()"
            color="rgb(233, 105, 30)"
            style="margin-top: -15px;"
            >등록</v-btn
          >
        </div>
        <hr />
      </div>
    </div>
    <div class="review-sort" style="display:inline;">
      <v-row>
        <h2 style="text-align:left; width: fit-content;">
          리뷰({{ review_cnt }}개)
        </h2>
        <v-spacer></v-spacer>
        <span
          @click="
            getReview();
            selectTab();
          "
          class="tab"
          style="cursor:pointer; color:rgb(233, 105, 30)"
          >최신순</span
        >
        <span style="margin: 0px 5px">|</span>
        <span
          @click="
            getReviewHighScore();
            selectTab();
          "
          class="tab"
          style="cursor:pointer;"
          >높은 평점순</span
        >
        <span style="margin: 0px 5px">|</span>
        <span
          @click="
            getReviewLowScore();
            selectTab();
          "
          class="tab"
          style="cursor:pointer;"
          >낮은 평점순</span
        >
      </v-row>
    </div>
    <div
      class="review-origin"
      v-for="(review, index) in reviews"
      :key="review.id"
    >
      <div style="border: 1px solid silver; border-radius: 0.4em">
        <article class="review review-1">
          <v-row>
            <h3
              v-if="review.user === null"
              class="review-title"
              style="display: inline; margin-right: 2px;"
            >
              {{ review.userid }}
            </h3>
            <h3 v-else class="review-title" style="margin-right: 2px;">
              {{ review.user.username }}
            </h3>
            <v-rating
              :value="review.score"
              readonly
              background-color="orange lighten-3"
              color="orange"
              dense="true"
              half-increments="true"
              small="true"
            ></v-rating>
            <br />
            <v-spacer></v-spacer>
            <p style="color: lightgray">{{ review.created_at.slice(0, 10) }}</p>
            <p
              v-show="review.user !== null && review.user.id == loginUserId"
              @click="clickedDeleteReview(review.id)"
              style="cursor:pointer; margin-left:3px;"
            >
              <img
                src="../assets/image/delete.png"
                style="width:15px;"
                alt=""
              />
            </p>
          </v-row>
          <p class="review-excerpt" style="margin-bottom: 10px">
            {{ review.content }}
          </p>

          <!-- 답글 달기 -->
          <v-row justify="center" v-show="storeOwner == loginUserId">
            <v-expansion-panels
              v-show="review.replyset.length == 0 && loginUsertype == 0"
            >
              <v-expansion-panel style="margin-top: 40px;">
                <v-expansion-panel-header>답글 달기</v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-textarea
                    outlined
                    v-model="myComment[index]"
                    name="input-7-4"
                    label="답글을 남겨보세요."
                    color="orange"
                  ></v-textarea>
                  <div class="text-right" style="margin-top: -15px">
                    <v-btn
                      v-show="myComment[index] != 0"
                      @click="
                        registerComment(index, review.id, myComment[index])
                      "
                      color="orange"
                      >등록</v-btn
                    >
                  </div>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-row>

          <v-row
            v-if="review.replyset.length > 0"
            class="comment"
            style="margin-top:-10px"
          >
            <div class="chat" style="background: none;">
              <div class="chat-history">
                <div class="message-data">
                  <div class="message my-message">
                    <v-row>
                      <span
                        class="message-data-name"
                        style="font-size: 20px; margin-bottom: 5px;"
                        >사장님</span
                      >
                      <span class="message-data-time">{{
                        review.replyset.slice(-1)[0].created_at.substring(0, 10)
                      }}</span>
                      <v-spacer></v-spacer>
                      <img
                        v-show="storeOwner == loginUserId"
                        src="../assets/image/delete.png"
                        style="width:15px; height:15px; cursor: pointer"
                        alt=""
                        @click="
                          clickedDeleteComment(
                            review.id,
                            review.replyset.slice(-1)[0].id
                          )
                        "
                      />
                    </v-row>
                    <v-row>
                      <span>{{ review.replyset.slice(-1)[0].content }}</span>
                    </v-row>
                  </div>
                </div>
              </div>
            </div>
          </v-row>
        </article>
      </div>
      <br />
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
// const baseURL = "http://127.0.0.1:8000/";
const baseURL = "http://ec2-52-79-239-80.ap-northeast-2.compute.amazonaws.com/";

export default {
  data() {
    return {
      show: false,
      rating: 0,
      reviews: [],
      review_cnt: 0,
      myReview: "",
      flag: 1,
      myComment: [],
      loginUsertype: 0,
      loginUserId: 0,
      reviewUsertype: 0,
      reviewUserId: 0,
      clicked: false,
      storeOwner: 0,
    };
  },
  watch: {
    clicked() {
      if (this.flag == 1) {
        this.getReview();
      } else if (this.flag == 2) {
        this.getReviewHighScore();
      } else {
        this.getReviewLowScore();
      }
      this.clicked = false;
    },
  },
  created() {
    this.getReview();
    this.getUserInfo();
    this.getStoreInfo();
  },

  computed: {
    ...mapGetters("server", ["getBaseURL"]),
  },

  methods: {
    getStoreInfo() {
      const storeid = this.$route.params.storeid;
      axios
        .post(baseURL + `api/stores/${storeid}/`, null, {
          headers: {
            Authorization: `Token ${this.$cookies.get("auth-token")}`,
          },
        })
        .then((res) => {
          this.storeOwner = res.data.user;
        });
    },

    // 로그인한 유저 프로필
    getUserInfo() {
      axios
        .post(baseURL + "api/accounts/profile/", null, {
          headers: {
            Authorization: `Token ${this.$cookies.get("auth-token")}`,
          },
        })
        .then((res) => {
          this.loginUsertype = res.data.usertype;
          this.loginUserId = res.data.id;
        });
    },

    // 리뷰 분류 탭 변경
    selectTab() {
      var tab = document.getElementsByClassName("tab");
      for (var i = 0; i < tab.length; i++) {
        tab[i].addEventListener("click", function() {
          for (var j = 0; j < tab.length; j++) {
            tab[j].style.color = "black";
          }
          this.style.color = "rgb(233, 105, 30)";
        });
      }
    },

    getReview() {
      this.flag = 1;
      axios
        .post(
          baseURL + "api/reviews/store_review_list/",
          {
            storeid: this.$route.params.storeid,
          },
          {
            headers: {
              Authorization: `Token ${this.$cookies.get("auth-token")}`,
            },
          }
        )
        .then((res) => {
          this.reviews = [];
          this.review_cnt = 0;
          for (var i = 0; i < res.data.length; i++) {
            if (
              res.data[i].content.trim() == "" ||
              res.data[i].content.trim() == null
            )
              continue;
            this.reviews.push(res.data[i]);
            this.review_cnt += 1;
            if (res.data.user == null) {
              this.reviewUserId = res.data.userid;
            } else {
              this.reviewUserId = res.data.user.id;
            }
          }
        })
        .catch((err) => {
          console.log("리뷰 안온다" + err);
        });
    },

    getReviewHighScore() {
      this.flag = 2;
      axios
        .post(
          baseURL + "api/reviews/sort_review_high_score/",
          {
            storeid: this.$route.params.storeid,
          },
          {
            headers: {
              Authorization: `Token ${this.$cookies.get("auth-token")}`,
            },
          }
        )
        .then((res) => {
          this.reviews = res.data;
          this.review_cnt = res.data.length;
        });
    },

    getReviewLowScore() {
      this.flag = 3;
      axios
        .post(
          baseURL + "api/reviews/sort_review_low_score/",
          {
            storeid: this.$route.params.storeid,
          },
          {
            headers: {
              Authorization: `Token ${this.$cookies.get("auth-token")}`,
            },
          }
        )
        .then((res) => {
          this.reviews = res.data;
          this.review_cnt = res.data.length;
        });
    },

    msg() {
      if (this.myReview.length == 0 && this.rating == 0) {
        alert("평점과 리뷰를 평가해주세요.");
        return;
      } else if (this.myReview.length == 0) {
        alert("최소 한 글자 이상 작성해주세요.");
        return;
      } else if (this.rating == 0) {
        alert("평점을 매겨주세요.");
        return;
      }
      this.clicked = true;
    },

    msgComment() {
      alert("답글을 남겨주세요.");
    },

    registerReview() {
      axios
        .post(
          baseURL + "api/reviews/create_review/",
          {
            storeid: this.$route.params.storeid,
            content: this.myReview,
            score: this.rating,
          },
          {
            headers: {
              Authorization: `Token ${this.$cookies.get("auth-token")}`,
            },
          }
        )
        .then((res) => {
          this.clicked = true;
        })
        .catch((err) => {
          console.log(err.response);
        });
      this.myReview = "";
      this.rating = 0;
    },

    clickedDeleteReview(reviewId) {
      var answer = confirm("리뷰를 삭제하시겠습니까?");
      if (answer) {
        axios
          .delete(baseURL + `api/reviews/${reviewId}/`, {
            headers: {
              Authorization: `Token ${this.$cookies.get("auth-token")}`,
            },
          })
          .then((res) => {
            this.clicked = true;
          })
          .catch((err) => {
            alert("리뷰 삭제 실패!");
          });
      }
    },

    // 사장님 답글 등록
    registerComment(index, reviewId, content) {
      axios
        .post(
          baseURL + `api/reviews/${reviewId}/create_reply/`,
          {
            content: content,
          },
          {
            headers: {
              Authorization: `Token ${this.$cookies.get("auth-token")}`,
            },
          }
        )
        .then((res) => {
          this.getReview();
          this.myComment[reviewId] = "";
          this.clicked = true;
        })
        .catch((err) => {
          console.log("답글ㄴㄴ", err.response);
        });
    },

    clickedDeleteComment(reviewId, commentId) {
      var answer = confirm("답글을 삭제하시겠습니까?");
      if (answer) {
        axios
          .post(
            baseURL + `api/reviews/${reviewId}/reply/${commentId}/`,
            {
              storeid: this.$route.params.storeid,
            },
            {
              headers: {
                Authorization: `Token ${this.$cookies.get("auth-token")}`,
              },
            }
          )
          .then((res) => {
            this.clicked = true;
          })
          .catch((err) => {});
      }
    },
  },
};
</script>

<style scoped>
* {
  position: relative;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  border: none;
}
h2,
h3 {
  font-size: 1em;
}
span {
  font-size: 0.8em;
}
p {
  font-size: 0.7em;
  color: #444;
  line-height: 1.3em;
}
a {
  text-decoration: none;
}
.wrapper {
  width: 800px;
  margin: 0 auto;
  padding: 0;
  position: relative;
}
.content {
  padding: 20px 0;
  width: 60%;
  float: left;
}
.review {
  margin-bottom: 30px;
  border: 2px solid transparent;
  box-sizing: border-box;
  margin: -10px;
  padding: 20px;
  text-align: left;
}

.chat {
  width: 100%;
  float: left;
  border-top-right-radius: 5px;
  border-bottom-right-radius: 5px;
  border-color: transparent;
  color: #434651;
  background-color: none;
}

.chat .chat-about {
  float: left;
  padding-left: 10px;
  margin-top: 6px;
}
.chat .chat-with {
  font-weight: bold;
  font-size: 16px;
}
.chat .chat-history .message-data {
  margin-bottom: 15px;
}
.message-data-time {
  color: #a8aab1;
  padding-left: 6px;
  font-size: 13px;
  float: right;
  margin-right: 10px;
}
.chat .chat-history .message {
  color: black;
  padding: 18px 20px;
  line-height: 26px;
  font-size: 16px;
  border-radius: 7px;
  width: 100%;
  position: relative;
}
.chat .chat-history .message:after {
  bottom: 100%;
  left: 2%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
  border-bottom-color: #ededed;
  border-width: 10px;
  margin-left: -10px;
}
.chat .chat-history .my-message {
  background: #ededed;
}
</style>
