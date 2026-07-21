def human_review(result: dict) -> dict:
    
    print("\n" + "="*50)
    print("HUMAN REVIEW REQUIRED")
    print("="*50)
    print(f"\nQuestion: {result['question']}")
    print(f"\nAgent used: {result['agent']}")
    print(f"\nAnswer:\n{result['answer']}")
    print("\n" + "-"*50)
    
    # Ask human to approve
    decision = input("\nApprove this answer? (yes/no): ").strip().lower()
    
    if decision == "yes":
        result['approved'] = True
        result['status'] = "APPROVED ✅"
        print("Answer approved!")
    else:
        correction = input("Enter correct answer: ").strip()
        result['answer'] = correction
        result['approved'] = True
        result['status'] = "CORRECTED ✅"
        print("Answer corrected!")
    
    return result