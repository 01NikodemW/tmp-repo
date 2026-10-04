import { describe, expect, it } from 'vitest'
import { selectTodos, validateTodo } from './todos'
import type { Todo } from '../types'

const base: Todo = {
  id: 1,
  title: 'Sprint plan',
  description: '',
  priority: 'medium',
  completed: false,
  due_date: null,
  created_at: '2026-10-01T12:00:00Z',
  updated_at: '2026-10-01T12:00:00Z',
}

describe('selectTodos', () => {
  it('combines status with a case-insensitive search in the description', () => {
    const matching = { ...base, description: 'Discuss the API' }
    const todos = [
      matching,
      { ...matching, id: 2, completed: true },
      { ...base, id: 3 },
    ]
    expect(selectTodos(todos, 'active', ' api ', 'newest')).toEqual([matching])
  })

  it('sorts by priority without changing the source array', () => {
    const high: Todo = { ...base, id: 2, priority: 'high' }
    const todos = [base, high]
    expect(selectTodos(todos, 'all', '', 'priority')).toEqual([high, base])
    expect(todos).toEqual([base, high])
  })
})

describe('validateTodo', () => {
  const input = { title: 'Plan', description: '', priority: 'medium' as const, due_date: '' }

  it('rejects a title containing a line break', () => {
    expect(validateTodo({ ...input, title: 'Plan\nsprint' }).title).toBe(
      'The task title must be a single line.',
    )
    expect(validateTodo({ ...input, title: 'Plan\r\nsprint' }).title).toBe(
      'The task title must be a single line.',
    )
  })

  it('ignores surrounding line breaks in a single-line title', () => {
    expect(validateTodo({ ...input, title: '\n Plan \n' }).title).toBeUndefined()
  })
})
