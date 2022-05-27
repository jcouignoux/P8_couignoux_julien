var starBlocks = document.querySelectorAll('.star-block').forEach(starBlock => {
    starBlock.addEventListener('mouseover', (event)=>{
        event.preventDefault()
        // post = starBlock.nextElementSibling.value
        // console.log(post)
        post_id = starBlock.id.replace('star-block', '')
        var zero = document.getElementById('zero' + post_id)
        var one = document.getElementById('first' + post_id)
        var two = document.getElementById('second' + post_id)
        var three = document.getElementById('third' + post_id)
        var four = document.getElementById('fourth' + post_id)
        var five = document.getElementById('fifth' + post_id)
        
        var input_star = document.querySelector('#test'+ post_id)
        
        var handleStarSelect = (size) => {
            var children = document.getElementById('star-block' + post_id).children
            for (let i=1; i < children.length; i++) {
                if (i <= size) {
                    children[i].classList.add('checked')
                } else {
                    children[i].classList.remove('checked')
                }
            }
        }
        
        var handSelect = (selection) => {
            switch(selection) {
                case 'zero' + post_id: {
                    handleStarSelect(0)
                    return
                }
                case 'first' + post_id: {
                    handleStarSelect(1)
                    return
                }
                case 'second' + post_id: {
                    handleStarSelect(2)
                    return
                }
                case 'third' + post_id: {
                    handleStarSelect(3)
                    return
                }
                case 'fourth' + post_id: {
                    handleStarSelect(4)
                    return
                }
                case 'fifth' + post_id: {
                    handleStarSelect(5)
                    return
                }
            }
        }
        
        var getNumericValue = (stringValue) => {
            let numericValue
            if (stringValue.startsWith('zero')) {
                numericValue = 0
            }
            else if (stringValue.startsWith('first')) {
                numericValue = 1
            }
            else if (stringValue.startsWith('second')) {
                numericValue = 2
            }
            else if (stringValue.startsWith('third')) {
                numericValue = 3
            }
            else if (stringValue.startsWith('fourth')) {
                numericValue = 4
            }
            else if (stringValue.startsWith('fifth')) {
                numericValue = 5
            }
            return numericValue
        }
        
        var arr = [zero, one, two, three, four, five]
        if (zero) {
            // handleStarSelect(post)
            arr.forEach(item => item.addEventListener('click', (event)=>{
                var val = event.target.id
                var val_num = getNumericValue(val)
                handSelect(val)
                input_star.value = val_num
            }))
        }
    })
})
