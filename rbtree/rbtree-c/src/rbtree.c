#include "include/rbtree.h"

#include <stdlib.h>

typedef enum rb_color {
    RB_RED = 0,
    RB_BLACK = 1,
} rb_color_t;

typedef struct rb_node {
    int key;
    void* value;
    rb_color_t color;
    struct rb_node* left;
    struct rb_node* right;
    struct rb_node* parent;
} rb_node_t;

struct rb_tree {
    rb_node_t* root;
    rb_node_t* nil;
    size_t size;
    void (*destroy_value)(void* value);
};

static rb_node_t* CreateSentinel(void) {
    rb_node_t* nil = (rb_node_t*)malloc(sizeof(*nil));
    if (nil == NULL) {
        return NULL;
    }

    nil->key = 0;
    nil->value = RB_BLACK;
    nil->left = nil;
    nil->right = nil;
    nil->parent = nil;
    return nil;
}

static void DestroyStoredValue(const rb_tree_t* tree, void* value) {
    if (tree->destroy_value != NULL && value != NULL) {
        tree->destroy_value(value);
    }
}

static void DestroySubtree(rb_tree_t* tree, rb_node_t* node) {
    if (node == tree->nil) {
        return;
    }

    DestroySubtree(tree, node->left);
    DestroySubtree(tree, node->right);
    DestroyStoredValue(tree, node->value);
    free(node);
}

static void LeftRotate(rb_tree_t* tree, rb_node_t* x) {
    rb_node_t* y = x->right;

    x->right = y->left;
    if (y->left != tree->nil) {
        y->left->parent = x;
    }

    y->parent = x->parent;
    if (x->parent == tree->nil) {
        tree->root = y;
    } else if (x == x->parent->left) {
        x->parent->left = y;
    } else {
        x->parent->right = y;
    }

    y->left = x;
    x->parent = y;
}