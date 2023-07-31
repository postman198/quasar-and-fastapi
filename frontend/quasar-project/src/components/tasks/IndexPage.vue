<template>
  <div align="center" class="row" style="height: 90vh">
    <div v-bind:class="{'justify-center': $q.screen.xl || $q.screen.md || $q.screen.sm ||$q.screen.xs}"
         class="col-12 col-md-16 flex content-center">
      <q-card v-bind:style="$q.screen.lt.sm ? {'width': '60%'} : {'width': '100%'}">
        <q-btn label="Add Task" color="primary" @click="promptAddTask = true" />
        <q-dialog v-model="promptAddTask" persistent>
          <q-card style="min-width: 350px">
            <q-bar>
              <q-btn dense flat icon="close" v-close-popup>
                <q-tooltip>Close</q-tooltip>
              </q-btn>
            </q-bar>
            <q-card-section>
              <div class="text-h6">New Task</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
              <q-input
              outlined
              label="Enter task title *"
              v-model="addTaskForm.title.value"
              @update:model-value="isInputValid"
              @blur="isInputValid"
              :error="addTaskForm.title.error"
              :error-message="addTaskForm.title.msg"
              autofocus
              @keyup.enter="promptAddTask = false" />
              <q-input
              outlined
              label="Enter task description *"
              v-model="addTaskForm.description"
              type="textarea"
              autofocus
              @keyup.enter="promptAddTask = false" />
            </q-card-section>

            <q-card-actions align="right" class="text-primary">
              <q-btn flat label="Cancel" v-close-popup />
              <q-btn flat label="Add Task" v-close-popup @click="addNewTask"/>
            </q-card-actions>
          </q-card>
        </q-dialog>
        <q-card-section align="center" v-if="!(tasks.length > 0)">
          <div>
            <h1>No task available</h1>
          </div>
        </q-card-section>
        <q-card-section align="center" v-if="tasks.length > 0">
          <div>
            <q-table
              flat bordered
              title="Your Tasks List"
              :rows="tasks"
              :columns="columns"
              row-key="id"
              dark
            >
              <template v-slot:body="props">
                <q-tr
                  v-bind="props.rowProps"
                  class="cursor-pointer"
                >
                  <q-td v-for="col in props.cols" :key="col.name" :props="props">
                    {{ col.value }}
                  </q-td>
                  <q-td>
                    <q-icon
                      name="edit"
                      class="q-mr-md"
                      @click="editTask(props.row)"
                    />
                    <q-dialog v-model="promptEditTask" persistent>
                      <q-card style="min-width: 350px">
                        <q-bar>
                          <q-btn dense flat icon="close" v-close-popup>
                            <q-tooltip>Close</q-tooltip>
                          </q-btn>
                        </q-bar>
                        <q-card-section>
                          <div class="text-h6">Edit Task</div>
                        </q-card-section>

                        <q-card-section class="q-pt-none">
                          <q-input
                          outlined
                          label="Task title:"
                          v-model="editTaskForm.title.value"
                          @update:model-value="isInputValidEdit"
                          @blur="isInputValidEdit"
                          :error="editTaskForm.title.error"
                          :error-message="editTaskForm.title.msg"
                          autofocus
                          @keyup.enter="promptEditTask = false" />
                          <q-input
                          outlined
                          label="Task description:"
                          v-model="editTaskForm.description"
                          type="textarea"
                          autofocus
                          @keyup.enter="promptEditTask = false" />
                          <q-input
                          outlined
                          label="Task status:"
                          v-model="editTaskForm.status"
                          autofocus
                          @keyup.enter="promptEditTask = false" />
                        </q-card-section>

                        <q-card-actions align="right" class="text-primary">
                          <q-btn flat label="Cancel" v-close-popup />
                          <q-btn flat label="Update Task" v-close-popup @click="updateChosenTask"/>
                        </q-card-actions>
                      </q-card>
                    </q-dialog>
                    <q-icon
                      name="delete"
                      class="q-mr-md"
                      @click.stop="deleteTask(props.row.id)"
                    />
                    <q-dialog v-model="alertDeleteTask">
                      <q-card>
                        <q-bar>
                          <q-btn dense flat icon="close" v-close-popup>
                            <q-tooltip>Close</q-tooltip>
                          </q-btn>
                        </q-bar>
                        <q-card-section>
                          <div class="text-h6">Alert</div>
                        </q-card-section>

                        <q-card-section class="q-pt-none">
                          Are you sure you want to delete the task?
                        </q-card-section>

                        <q-card-actions align="right">
                          <q-btn flat label="Delete" color="primary" v-close-popup @click="removeChosenTask"/>
                        </q-card-actions>
                      </q-card>
                    </q-dialog>
                  </q-td>
                </q-tr>
              </template>
            </q-table>

          </div>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import { useQuasar } from 'quasar'
import { mapGetters, mapActions } from 'vuex'
import { validateInput } from 'src/hooks'

let $q
const columns = [
  { name: 'title', required: true, label: 'Title of task', align: 'left', field: task => task.title, format: val => `${val}`, sortable: true },
  { name: 'description', align: 'center', label: 'Task Description', field: 'description', sortable: true },
  { name: 'fastatust', label: 'Task status (Open/Done)', field: 'status', sortable: true }
]
export default {
  name: 'IndexPage',
  data () {
    return {
      promptAddTask: false,
      promptEditTask: false,
      alertDeleteTask: false,
      taskIdToDelete: '',
      addTaskForm: {
        title: {
          value: '',
          requiredMsg: 'title is required!',
          required: true
        },
        description: '',
        status: 'Open'
      },
      isInputValid: () => {
        return validateInput(this.addTaskForm, 'title')
      },
      editTaskForm: {
        id: '',
        title: {
          value: '',
          requiredMsg: 'title is required!',
          required: true
        },
        description: '',
        status: ''
      },
      isInputValidEdit: () => {
        return validateInput(this.editTaskForm, 'title')
      },
      columns,
      selectedRow: null
    }
  },
  computed: {
    tasks () {
      return this.getTasks
    },
    ...mapGetters('auth', ['getTasks'])
  },
  mounted () {
    $q = useQuasar()
  },
  methods: {
    ...mapActions('auth', ['addTask', 'updateTask', 'removeTask']),
    async addNewTask () {
      if (!this.addTaskForm.title.value) {
        $q.notify({
          type: 'negative',
          message: 'title feild is required!'
        })
      } else {
        try {
          const payload = {
            title: this.addTaskForm.title.value,
            description: this.addTaskForm.description,
            status: this.addTaskForm.status
          }
          await this.addTask(payload)
        } catch (err) {
          console.log(err)
          if (err.response.data.detail) {
            $q.notify({
              type: 'negative',
              message: err.response.data.detail
            })
          }
        }
      }
    },
    async editTask (task) {
      this.editTaskForm.id = task.id
      this.editTaskForm.title.value = task.title
      this.editTaskForm.status = task.status
      this.editTaskForm.description = task.description
      this.promptEditTask = true
    },
    async updateChosenTask () {
      if (!this.editTaskForm.title.value) {
        $q.notify({
          type: 'negative',
          message: 'title feild is required!'
        })
      } else {
        try {
          const task = {
            title: this.editTaskForm.title.value,
            description: this.editTaskForm.description,
            status: this.editTaskForm.status,
            id: this.editTaskForm.id
          }
          await this.updateTask(task)
        } catch (err) {
          console.log(err)
          if (err.response.data.detail) {
            $q.notify({
              type: 'negative',
              message: err.response.data.detail
            })
          }
        }
      }
    },
    deleteTask (id) {
      this.taskIdToDelete = id
      this.alertDeleteTask = true
    },
    async removeChosenTask () {
      if (!this.taskIdToDelete) {
        $q.notify({
          type: 'negative',
          message: 'task id is required!'
        })
      } else {
        try {
          await this.removeTask(this.taskIdToDelete)
        } catch (err) {
          console.log(err)
          if (err.response.data.detail) {
            $q.notify({
              type: 'negative',
              message: err.response.data.detail
            })
          }
        }
      }
    }
  }
}

</script>
