<template>

    <h3>作者分类信息</h3>

    <table border="1" width="600px">

        <tr>
            <th>作者ID</th>
            <th>作者姓名</th>
            <th>作者简介</th>

        </tr>

        <tr>
            <td>1</td>
            <td>余华</td>
            <td>当代作家，代表作《活着》《许三观卖血记》</td>
        </tr>

        <tr>
            <td>2</td>
            <td>刘慈欣</td>
            <td>科幻作家，代表作《三体》《流浪地球》</td>
        </tr>

        <tr>
            <td>3</td>
            <td>莫言</td>
            <td>诺贝尔文学奖获得者，代表作《红高粱》</td>
        </tr>


    </table>

    <el-card style="max-width: 70%">
        <template #header>
            <div class="card-header">
                <p>书籍类信息</p>
                <el-input v-model="search_message" style="width: 240px" placeholder="Please input"
                    @keyup.enter="sousuo" /> <el-button @click="sousuo">搜索</el-button>
                <el-button type="primary" @click="view">
                    新增书籍
                </el-button>
            </div>
        </template>

        <p>
            <el-table :data="tableData" style="width: 100%">
                <el-table-column prop="id" label="数据编号" width="120" />
                <el-table-column prop="title" label="书名" width="180" />
                <el-table-column prop="author_name" label="所属作者" width="140" />
                 <el-table-column prop="price" label="价格" width="140" />

                <el-table-column label="操作" width="150">
                    <template #default="scope">
                        <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
                        <el-button size="small" type="danger" @click="handleDelete(scope.row.id)">删除</el-button>

                    </template>
                </el-table-column>
            </el-table>

        </p>
        <template #footer>
              <el-pagination layout="prev, pager, next" :total="5" />
        </template>
    </el-card>

    <el-dialog v-model="dialogFormVisible" :title="edit_id=='' ?'新增书籍':'修改书籍'" width="500">
        <el-form :model="form">
            <el-form-item label="书籍名称" :label-width="formLabelWidth">
                <el-input v-model="form.title" autocomplete="off" />
            </el-form-item>

             <el-form-item label="所属作者" :label-width="formLabelWidth">
                <el-input v-model="form.author_id" autocomplete="off" />
            </el-form-item>

             <el-form-item label="价格" :label-width="formLabelWidth">
                <el-input v-model="form.price" autocomplete="off" />
            </el-form-item>
         
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="handleClick">
                    确认
                </el-button>
            </div>
        </template>
    </el-dialog>

</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import service from './router/index.js'
import { ElMessage, ElMessageBox } from 'element-plus'
const tableData = ref([])
const search_message = ref('')
const page = ref(1)
const dialogFormVisible= ref(false)
const formLabelWidth = '140px'
const form = reactive({
    title: '',
    author_id: '',
    price: ''
})

onMounted(() => {
    loadData()
})

const loadData = async () => {
    const params = {
        page: page.value,
        page_size: 10,
    }
    if (search_message.value) {
        params['keywords'] = search_message.value
    }


    const res = await service.get('/books', { params })
    console.log(res)
    tableData.value = res.data.items
}

const sousuo = () => {
    loadData()

}

const edit_id=ref('')
const view = () => {
    if (edit_id.value) {
        form.title=''
        form.author_id=''
        form.price=''
    }
    dialogFormVisible.value = true
}

const handleClick =async () => {
    if (edit_id.value){
        await service.put(`/books/${edit_id.value}`, form)
    }
    else{
        await service.post('/books', form) 
    }
    
    
    loadData()
    dialogFormVisible.value = false


}

const handleDelete=async(id)=>{

      ElMessageBox.confirm(
    '是否确定删除当前书籍信息?',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async() => {
        await service.delete(`/books/${id}`)
        loadData()
      ElMessage({
        type: 'success',
        message: '删除成功',
      })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消成功',
      })
    })
}

const handleEdit=(row)=>{
    edit_id.value=row.id
    Object.assign(form,{
        title:row.title,
        author_id:row.author_id,
        price:row.price
    
    })
    dialogFormVisible.value = true

}


</script>