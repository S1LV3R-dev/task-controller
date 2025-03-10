export class TASK_STATUS {
  static NEW = 0
  static PICKED = 1
  static FINISHED = 2
  static CANCELLED = -1

  static dict = {
    [TASK_STATUS.NEW]: 'New',
    [TASK_STATUS.PICKED]: 'Active',
    [TASK_STATUS.FINISHED]: 'Finished',
    [TASK_STATUS.CANCELLED]: 'Cancelled',
  }
}
