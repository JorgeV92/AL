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

static void RightRotate(rb_tree_t* tree, rb_node_t* y) {
    rb_node_t* x = y->left;

    y->left = x->right;
    if (x->right != tree->nil) {
        x->right->parent = y;
    }

    x->parent = y->parent;
    if (y->parent == tree->nil) {
        tree->root = x;
    } else if (y == y->parent->left) {
        y->parent->left = x;
    } else {
        y->parent->right = x;
    }

    x->right = y;
    y->parent = x;
}

static void InsertFixup(rb_tree_t* tree, rb_node_t* node) {
    while (node->parent->color == RB_RED) {
        if (node->parent == node->parent->parent->left) {
            rb_node_t* uncle = node->parent->parent->right;
            if (uncle->color == RB_RED) {
                node->parent->color = RB_BLACK;
                uncle->color = RB_BLACK;
                node->parent->parent->color = RB_RED;
                node = node->parent->parent;
            } else {
                if (node == node->parent->right) {
                    node = node->parent;
                    LeftRotate(tree, node);
                }
                node->parent->color = RB_BLACK;
                node->parent->parent->color = RB_RED;
                RightRotate(tree, node->parent->parent);
            }
        } else {
            rb_node_t* uncle = node->parent->parent->left;
            if (uncle->color == RB_RED) {
                node->parent->color = RB_BLACK;
                uncle->parent->color = RB_BLACK;
                node->parent->parent->color = RB_RED;
                node = node->parent->parent;
            } else {
                if (node == node->parent->left) {
                    node = node->parent;
                    RightRotate(tree, node);
                }
                node->parent->color = RB_BLACK;
                node->parent->parent->color = RB_RED;
                LeftRotate(tree, node->parent->parent);
            }
        }
    }

    tree->root->color = RB_BLACK;
}

static rb_node_t* FindNode(const rb_tree_t* tree, int key) {
    rb_node_t* curr = tree->root;

    while (curr != tree->nil) {
        if (key < curr->key) {
            curr = curr->left;
        } else if (key > curr->key) {
            curr = curr->right;
        } else {
            return curr;
        }
    }

    return tree->nil;
}

