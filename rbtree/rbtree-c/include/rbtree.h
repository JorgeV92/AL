#ifndef RBTREE_RBTREE_C
#define RBTREE_RBTREE_C

#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct rb_tree rb_tree_t;

typedef enum rb_status {
    RB_STATUS_OK = 0,
    RB_STATUS_DUPLICATE_KEY = 1,
    RB_STATUS_ALLOCATION_FAILED = 2,
    RB_STATUS_INVALID_ARGUMENT = 3,
} rb_status_t;

typedef void (*rb_visit_fn)(int key, void* value, void* user_data);

rb_tree_t* rb_tree_create(void (*destroy_value)(void* value));

void rb_tree_destroy(rb_tree_t* tree);

rb_status_t rb_tree_insert(rb_tree_t* tree, int key, void* value,
                            bool replace_existing);

void* rb_tree_find(const rb_tree_t* tree, int key);

bool rb_tee_contains(const rb_tree_t* tree, int key);

bool rb_tree_erase(rb_tree_t* tree, int key);

size_t rb_tree_size(const rb_tree_t* tree);

bool rb_tree_empty(const rb_tree_t* tree);

void rb_tree_inorder(const rb_status_t* tree, rb_visit_fn visit, void* user_data);

bool rb_tree_validate(const rb_status_t* tree);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif