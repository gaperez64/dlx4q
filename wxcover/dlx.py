def algox(wincmat, w=1):
    # There are either no rows or all remaining rows are soft constraints,
    # so we are done. The assumption is that the root always points to a
    # nonsoft column if one exists or None.
    if wincmat.root is None or wincmat.root.soft:
        yield w
        return
    head = wincmat.root
    # FIXME: Choose a column smartly

    # Iterate over rows sat-ing the col to extend partial solution
    satd = False
    it = head.below
    while it != head:
        oldroot = wincmat.root

        # we now remove all columns and rows related to the fixed
        # partial solution
        jt = it
        while True:
            col = jt.head
            # Find all rows with a 1 on this col
            kt = col.below
            while kt != col:
                # and remove the whole row (except for the
                # entries on the current column)
                lt = kt.right
                while True:
                    lt.above.below = lt.below
                    lt.below.above = lt.above
                    if lt.right == kt:
                        break
                    else:
                        lt = lt.right
                kt = kt.below
            # Remove column
            # NOTE: we only remove the header
            col.left.right = col.right
            col.right.left = col.left
            # NOTE: if we removed the root column, we update the root too
            if wincmat.root == col:
                if col.right == col:
                    wincmat.root = None
                else:
                    wincmat.root = col.right
            # Move to next column
            if jt.right == it:
                break
            else:
                jt = jt.right

        # FIXME: this is an invariant!
        # if wincmat.root is not None, we need to make sure it is
        # pointing to a nonsoft column if there is one
        # if wincmat.root is not None and wincmat.root.soft:
        #     rt = wincmat.root
        #     wincmat.root = wincmat.root.right
        #     while wincmat.root.soft and wincmat.root != rt:
        #         wincmat.root = wincmat.root.right
        #     assert wincmat.root == rt

        # At this point we can recursively count all solutions of the
        # subproblem
        for x in algox(wincmat, it.weight * w):
            yield x
            satd = True

        # then repair all removals (in reverse)
        wincmat.root = oldroot
        while True:
            col = jt.head
            # Repair column
            col.left.right = col
            col.right.left = col

            kt = col.above
            while kt != col:
                lt = kt.left
                while True:
                    # Repair row
                    lt.above.below = lt
                    lt.below.above = lt
                    if lt.left == kt:
                        break
                    else:
                        lt = lt.left
                kt = kt.above
            # Move to next column
            if jt == it:
                break
            else:
                jt = jt.left

        # move to the next row for another partial sol.
        # but only if this is not a cut column
        if head.cut and satd:
            break
        else:
            it = it.below
