
<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="24">
        <el-table v-if="loadcomplete"
                  :data="tableData.slice((currentPage-1)*pageSize,currentPage*pageSize)"
                  height="tableHeight"
                  style="width: 100%"
        >
          <el-table-column prop="title" label="推荐论文" width="400" :show-overflow-tooltip="true">
            <template v-slot="scope">
              <el-button type="text"
                         @click="openDialog(scope.row)"
              >
                {{ scope.row.title}}
              </el-button>
            </template>
          </el-table-column>
          <el-table-column prop="author" label="作者" width="200" :show-overflow-tooltip="true">
          </el-table-column>
          <el-table-column prop="summary" label="描述" show-overflow-tooltip>
          </el-table-column>
        </el-table>

      </el-col>

    </el-row>
    <div class="block">
      <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          v-model="currentPage"
          :page-size="pageSize"
          layout="prev, pager, next, jumper"
          :total="totalNum">
      </el-pagination>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      tableData:[],
      tableHeight: window.innerHeight  - 100,
      currentPage:1,
      pageSize:10,
      totalNum:100,
      username:'',
      loadcomplete: true,
    }
  },
  methods: {
    ///分页    初始页currentPage、初始每页数据数pagesize和数据testpage
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.pageSize = val;    //动态改变
    },
    handleCurrentChange(val) {
      //console.log(`当前页: ${val}`);
      console.log(this.totalNum);
      console.log((val-1)*this.pageSize);
      if(this.totalNum<=(val-1)*this.pageSize)
      {
        this.$message({
          message: "超出最大页码",
          type: 'warning',
        });
        return;
      }
      this.currentPage = val;
    },
    openDialog (paper) {
      console.log(`dash: ${paper.pdfLink}`);
      this.$router.push({
        name: 'readpage',
        params: {url:paper.pdfLink,id:paper.id}
      });
    },
    // eslint-disable-next-line no-unused-vars
    getData(qstr){
      this.username=localStorage.getItem('ms_username')
      let _this=this
      this.$http.request({
        url:_this.$url + '/getRecommendation?user='+_this.username,
        method:'get',
      }).then(function(response) {
        //console.log(response.data),
        _this.tableData = response.data.papers,
            _this.totalNum= response.data.len,
            _this.loadcomplete=true,
            console.log(_this.tableData)
        //console.log(_this.totalNum)
      }).catch(function(error) {
        console.log(error)
      });
    },
    defaultdata(){
      let _this=this
      this.$http.request({
        url:_this.$url + '/searchPaper?method=cat&query=cs.AI&maxNum=10',
        method:'get',
      }).then(function(response) {
        //console.log(response.data),
        _this.tableData = response.data.papers,
            _this.totalNum= response.data.num,
            _this.loadcomplete=true,
            console.log(_this.tableData)
        //console.log(_this.totalNum)
      }).catch(function(error) {
        console.log(error)
      });
    }

  },
  watch: {
  },
  created(){
    this.tabelData=new Array(this.pageSize);
    this.getData(this.$route.query);
    if(!this.loadcomplete)
      this.defaultdata();
  },
}
</script>
<style>
.el-tooltip__popper{max-width:40%}
</style>
<style scoped>
.el-row {
  top:4%;
  bottom: 4%;
  right:0px;
  width:100%;
  position: absolute;
  overflow-y: scroll;
  z-index:1;
}
.el-row ::-webkit-scrollbar {
  width: 0;
}
.el-row  > ul {
  height: 100%;
}
.block{
  bottom:0px;
  left: 50%;
  position:fixed;
  z-index:1;
}
</style>
